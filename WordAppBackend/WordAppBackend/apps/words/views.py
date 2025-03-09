import logging
import time
from datetime import timedelta

import requests
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet

from WordAppBackend.utils.paginations import GlobalPagination
from users.models import UserWordBandModel, UserWordRecordModel, DailyRecordModel
from words.models import CategoryModel, WordModel, WordBandModel, BandToWordModel
from words.serializers import CategorySerializer, WordBandSerializer, UserWordBandSerializer, UserWordBandGetSerializer, \
    WordListSerializer, WordDetailSerializer, DailyRecordSerializer
from words.utils import get_word_detail

# Create your views here.

logger = logging.getLogger('word')


class CategoryViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()
    permission_classes = (IsAuthenticated,)


class ImportWordBandView(APIView):

    def get(self, request):
        url = 'https://cdn.maimemo.com/cache/v2/books/1385974ed5904a438616ff7b/1710385755000.json'
        book_name = 'TOEFL词汇正序版'
        category = '托福'
        response = requests.get(url, verify=False)
        response = response.json()
        words = response.get("data").get('book').get('vocabulary')
        word_number = len(words)
        with transaction.atomic():
            word_band = WordBandModel.objects.create(name=book_name, category=CategoryModel.objects.get(name=category),
                                                     word_count=word_number,
                                                     is_builtin=True)
            for word in words:
                try:
                    word_obj = WordModel.objects.get(spelling=word.get('spelling'))
                except WordModel.DoesNotExist:
                    word_obj = WordModel.objects.create(spelling=word.get('spelling'))
                if not BandToWordModel.objects.filter(band=word_band, word=word_obj).exists():
                    BandToWordModel.objects.create(band=word_band, word=word_obj, order_number=word.get('order'))
            # print(words)
            number = BandToWordModel.objects.filter(band=word_band).count()
            word_band.word_count = number
            word_band.save()
        return Response()


class GetWordDetailView(APIView):

    def get(self, request):
        words = WordModel.objects.all()
        for word in words:
            if word.phrases:
                continue
            data = get_word_detail(word.spelling)
            if 'errmsg' in data:
                print(data['errmsg'], word.spelling)
                continue
                # return Response(data['errmsg'], status=status.HTTP_400_BAD_REQUEST)
            else:
                # 手动更新字段并保存
                for key, value in data.items():
                    setattr(word, key, value)  # 动态设置字段值
                word.save()  # 保存修改到数据库
            time.sleep(1)
        WordModel.objects.filter(phrases__isnull=True).delete()
        bands = WordBandModel.objects.all()
        for band in bands:
            count = BandToWordModel.objects.filter(band=band).count()
            band.word_count = count
            band.save()
        return Response({'message': 'ok'})


class WordBandViewSet(ReadOnlyModelViewSet):
    queryset = WordBandModel.objects.all()
    serializer_class = WordBandSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            return WordBandModel.objects.filter(category_id=category_id, is_builtin=True)
        else:
            return WordBandModel.objects.all()


class WordBandUserViewSet(ModelViewSet):
    # queryset = UserWordBandModel.objects.filter()
    # serializer_class = UserWordBandSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        is_builtin = self.request.query_params.get('is_builtin', None)
        if is_builtin is None:
            return UserWordBandModel.objects.filter(user=self.request.user)
        if is_builtin == 'true':
            return UserWordBandModel.objects.filter(user=self.request.user, word_band__is_builtin=True)
        elif is_builtin == 'false':
            return UserWordBandModel.objects.filter(user=self.request.user, word_band__is_builtin=False)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserWordBandGetSerializer
        return UserWordBandSerializer

    def perform_destroy(self, instance):
        if instance.word_band.is_builtin is False:
            instance.word_band.delete()
        super().perform_destroy(instance)

    @action(methods=['POST'], detail=False)
    def create_word_band(self, request, *args, **kwargs):
        """根据上传的文件创建词书"""
        txt_file = request.FILES.get('file')
        title = request.data.get('title')
        daily_goal = request.data.get('daily_goal')
        if not all([title, daily_goal]):
            return Response({'detail': 'title和daily_goal为必传'}, status=status.HTTP_400_BAD_REQUEST)
        if UserWordBandModel.objects.filter(user=request.user, word_band__name=title).exists():
            return Response({'detail': '词书title重复'}, status=status.HTTP_400_BAD_REQUEST)
        loaded_list = []
        for line_bytes in txt_file:  # 逐行读取二进制数据
            line = line_bytes.decode('utf-8').strip()  # 解码并去除空白
            loaded_list.append(line)
        with transaction.atomic():
            word_band = WordBandModel.objects.create(name=title, creator=request.user)
            band_word_lst = []
            number = 1
            for word in loaded_list:
                word = word.strip()
                if word == '':
                    continue
                try:
                    word = WordModel.objects.get(spelling=word)
                    band_word_lst.append(BandToWordModel(band=word_band, word=word, order_number=number))
                    number += 1
                except WordModel.DoesNotExist:
                    logger.error(f'单词{word}不存在')
                    continue
            BandToWordModel.objects.bulk_create(band_word_lst)
            instance = UserWordBandModel.objects.create(word_band=word_band, user=request.user,
                                                        daily_goal=int(daily_goal))
            word_band.word_count = len(band_word_lst)
            word_band.save()
            request.user.using_word_band = instance
            request.user.save()
        return Response(UserWordBandGetSerializer(instance).data)


class WordViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = GlobalPagination

    def get_queryset(self):
        word_band_id = self.request.query_params.get('word_band_id', None)
        if word_band_id:
            word_band_id = int(word_band_id)
            return WordModel.objects.filter(bands__band_id=word_band_id)
        return WordModel.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WordListSerializer
        return WordDetailSerializer

    @action(methods=['GET'], detail=False)
    def search_words(self, request):
        search_word = request.query_params.get('search_word', None)
        if not search_word:
            return Response({'detail': 'search_word为必传项'}, status=status.HTTP_400_BAD_REQUEST)
        words = WordModel.objects.filter(spelling__icontains=search_word).all()
        return Response(WordDetailSerializer(words, many=True).data)


class LearningProcessView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_next_word(self, user):
        # 优先获取需要复习的单词
        review_words = UserWordRecordModel.objects.filter(
            user=user,
            next_review__date__lte=timezone.now().date()
        ).exclude(memory_stage=5).order_by('next_review')

        if review_words.exists():
            return review_words.first().word  # 返回需要复习的单词

        # 检查用户是否选择词书
        using_word_band = user.using_word_band
        if not using_word_band:
            return None

        # 检查今日新词是否达标
        if using_word_band.today_studied >= using_word_band.daily_goal:
            return None

        # 获取当前词书未学单词
        learned_words = UserWordRecordModel.objects.filter(user=user).values_list('word', flat=True)
        new_words = BandToWordModel.objects.filter(
            band=using_word_band.word_band
        ).exclude(word__in=learned_words).order_by('order_number')

        return new_words.first().word if new_words.exists() else None

    def get(self, request, *args, **kwargs):
        user = request.user
        next_word = self.get_next_word(user)

        if not next_word:
            return Response({'message': '今日学习完成'}, status=status.HTTP_200_OK)

        # 返回单词详情和进度
        return Response({'word': WordDetailSerializer(next_word).data,
                         'process': f'{user.using_word_band.today_studied}/{user.using_word_band.daily_goal}'})

    def post(self, request):
        user = request.user
        word_id = request.data.get('word_id')
        is_correct = request.data.get('is_correct')

        # 更新用户学习记录
        record, created = UserWordRecordModel.objects.get_or_create(
            user=user,
            word_id=word_id,
            defaults={  # 默认值
                'memory_stage': 0,
                'next_review': timezone.now() + timedelta(days=1),  # 初始值设为1天后
                'correct_count': 0,
                'wrong_count': 0
            }
        )
        # 更新词书进度
        using_word_band = user.using_word_band
        if created and using_word_band:
            # 原子操作避免并发问题
            UserWordBandModel.objects.filter(pk=using_word_band.pk).update(
                today_studied=F('today_studied') + 1,
                study_words=F('study_words') + 1
            )
            # 刷新内存中的对象
            using_word_band.refresh_from_db()

        # 根据记忆算法更新状态（简化的SM-2算法）
        if is_correct:
            record.memory_stage += 1
            record.correct_count += 1
            interval = 2 ** record.memory_stage  # 间隔天数指数增长
        else:
            record.memory_stage = max(0, record.memory_stage - 1)
            record.wrong_count += 1
            interval = 1  # 错误则第二天复习

        record.next_review = timezone.now() + timedelta(days=interval)
        record.save()

        # 更新每日记录
        daily_record, _ = DailyRecordModel.objects.get_or_create(
            user=user,
            date=timezone.now().date()
        )

        if created:
            daily_record.new_words += 1
            user.studied_words += 1
        else:
            daily_record.review_words += 1
        user.today_words += 1
        user.save()
        daily_record.save()

        return Response({'message': '学习状态已更新'}, status=status.HTTP_200_OK)


class DailyRecordView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DailyRecordSerializer

    def get_queryset(self):
        return self.request.user.daily_records
