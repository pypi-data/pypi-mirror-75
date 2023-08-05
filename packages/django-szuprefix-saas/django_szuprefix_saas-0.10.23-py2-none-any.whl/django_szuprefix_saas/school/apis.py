# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django_szuprefix.api.mixins import BatchActionMixin
from django_szuprefix.auth.authentications import add_token_for_user
from django_szuprefix.utils.statutils import do_rest_stat_action

from .apps import Config

from . import models, mixins, serializers, importers, helper, stats
from rest_framework import viewsets, decorators, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_szuprefix.api.decorators import register

__author__ = 'denishuang'

@register()
class TeacherViewSet(mixins.SchoolMixin, viewsets.ModelViewSet):
    queryset = models.Teacher.objects.all()
    serializer_class = serializers.TeacherSerializer
    # permission_classes = [DjangoModelPermissionsWithView]
    filter_fields = {
        'id': ['in', 'exact'],
        'name': ['exact'],
        'user': ['exact']
    }
    search_fields = ('name', 'code')
    ordering_fields = ('name', 'code')

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_teacher)

@register()
class GradeViewSet(mixins.SchoolMixin, viewsets.ModelViewSet):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer

@register()
class SessionViewSet(mixins.SchoolMixin, viewsets.ModelViewSet):
    queryset = models.Session.objects.all()
    serializer_class = serializers.SessionSerializer
    search_fields = ('name', 'number')
    filter_fields = {'id': ['in', 'exact']}

    def perform_create(self, serializer):
        serializer.save(school=self.request.user.as_saas_worker.party.as_school)


@register()
class ClazzViewSet(mixins.SchoolMixin, viewsets.ModelViewSet):
    queryset = models.Clazz.objects.all()
    serializer_class = serializers.ClazzSerializer
    search_fields = ('name', 'code')
    filter_fields = {
        'id': ['in', 'exact'],
        'name': ['exact', 'endswith'],
        'code': ['exact'],
        'entrance_session': ['in', 'exact'],
        'grade': ['in', 'exact']
    }


    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ClazzSmallSerializer
        return super(ClazzViewSet, self).get_serializer_class()


    @decorators.list_route(['get'])
    def similar(self, request):
        q = request.query_params.get('q')
        import Levenshtein
        from django.db.models import F
        from django_szuprefix.utils.modelutils import CharCorrelation
        qset = self.filter_queryset(self.get_queryset()).values('name', a=CharCorrelation([F('name'), q])).filter(
            a__gt=0).order_by('-a').values_list('name', 'a')[:10]
        aa = [(Levenshtein.ratio(n, q), c, n) for n, c in qset]
        aa.sort(reverse=True)
        ss = [c for a, b, c in aa if a > 0.5]
        return Response({'similar': ss})

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_clazz)


@register()
class MajorViewSet(mixins.SchoolMixin, viewsets.ModelViewSet):
    queryset = models.Major.objects.all()
    serializer_class = serializers.MajorSerializer
    search_fields = ('name', 'code')
    filter_fields = {
        'code': ['exact'],
        'name': ['exact', 'in'],
        'id': ['in', 'exact'],
    }


@register()
class CollegeViewSet(mixins.SchoolMixin, viewsets.ModelViewSet):
    queryset = models.College.objects.all()
    serializer_class = serializers.CollegeSerializer
    search_fields = ('name', 'code')
    filter_fields = ('code', 'name',)


@register()
class ClazzCourseViewSet(mixins.PartyMixin, viewsets.ModelViewSet):
    queryset = models.ClazzCourse.objects.all()
    serializer_class = serializers.ClazzCourseSerializer
    search_fields = ('clazz__name', 'course__name')
    filter_fields = {
        'id': ['in', 'exact'],
        'clazz': ['exact'],
        'course': ['exact'],
        'teacher': ['exact']
    }


@register()
class StudentViewSet(mixins.SchoolMixin, BatchActionMixin, viewsets.ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    search_fields = ('name', 'number', 'code')
    filter_fields = {
        'id': ['in', 'exact'],
        'grade': ['exact'],
        'class': ['exact', 'in'],
        'number': ['exact', 'in'],
        'is_active': ['exact'],
        'is_bind': ['exact'],
        'is_formal': ['exact'],
        'class__id': ['exact', 'in'],
        'user': ['exact']
    }
    ordering_fields = ('name', 'number', 'create_time', 'grade', 'clazz')


    def get_permissions(self):
        if self.action in ['binding', 'trial_application']:
            return [IsAuthenticated()]
        return super(StudentViewSet, self).get_permissions()

    @decorators.list_route(['post'])
    def pre_import(self, request):
        importer = importers.StudentImporter(self.school)
        data = importer.clean(importer.get_excel_data(request.data['file']))
        return Response(data)

    @decorators.list_route(['post'])
    def post_import(self, request):
        importer = importers.StudentImporter(self.school)
        student, created = importer.import_one(request.data)
        return Response(self.get_serializer(instance=student).data,
                        status=created and status.HTTP_201_CREATED or status.HTTP_200_OK)

    @decorators.list_route(['POST'])
    def batch_active(self, request):
        return self.do_batch_action('is_active', True)

    @decorators.list_route(['POST'], permission_classes=[IsAuthenticated])
    def trial_application(self, request):
        helper.apply_to_be_student(request.user, request.data)
        return Response({'detail': 'ok'})

    @decorators.list_route(['post'], permission_classes=[IsAuthenticated])
    def binding(self, request):
        serializer = serializers.StudentBindingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            schools = serializer.save()
            data = serializer.data
            data['schools'] = schools
            add_token_for_user(data, request.user)
            return Response(data)
        else:
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.list_route(['POST'])
    def batch_unbind(self, request):
        return self.do_batch_action(helper.unbind)

    @decorators.list_route(['POST'])
    def batch_reset_password(self, request):
        return self.do_batch_action(helper.reset_password)

    @decorators.detail_route(['post'])
    def unbind(self, request):
        helper.unbind(self.get_object())
        return Response({'info': 'success'})

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_student)

