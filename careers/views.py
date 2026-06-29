from rest_framework import viewsets
from .serializers import CareerSerializer, StepSerializer, MaterialSerializer, ProgressSerializer, RegisterSerializer, SubcategorySerializer, TopicSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from collections import Counter
from .models import Career, Step, Material, Progress, Profile, Answer, Subcategory, Topic, Category

class CategoryWithSubsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Все категории с их подкатегориями
        categories = Category.objects.prefetch_related('subcategories').all()
        result = []
        for cat in categories:
            subs = Subcategory.objects.filter(category=cat)
            result.append({
                'id': cat.id,
                'title': cat.title,
                'icon': cat.icon,
                'subcategories': SubcategorySerializer(subs, many=True).data,
            })
        return Response(result)


class SubcategoryCareersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, subcategory_id):
        # Направления внутри подкатегории
        careers = Career.objects.filter(subcategory_id=subcategory_id)
        result = []
        for career in careers:
            result.append({
                'id': career.id,
                'title': career.title,
                'description': career.description,
                'icon': career.icon,
            })
        return Response(result)


class StepTopicsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, step_id):
        # Темы внутри шага
        try:
            step = Step.objects.get(id=step_id)
        except Step.DoesNotExist:
            return Response({'error': 'Не найдено'}, status=status.HTTP_404_NOT_FOUND)
        
        topics = Topic.objects.filter(step=step).order_by('order_num')
        return Response({
            'step_id': step.id,
            'step_title': step.title,
            'topics': TopicSerializer(topics, many=True).data,
        })

class ChooseCareerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, career_id):
        try:
            career = Career.objects.get(id=career_id)
        except Career.DoesNotExist:
            return Response({'error': 'Не найдено'}, status=status.HTTP_404_NOT_FOUND)

        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.active_career = career
        profile.save()

        return Response({
            'message': f'Вы выбрали курс: {career.title}',
            'career_id': career.id,
            'career_title': career.title,
        })


class MyActiveCareerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.active_career:
                career = profile.active_career
                steps = Step.objects.filter(career=career).order_by('order_num')
                
                completed_ids = set(
                    Progress.objects.filter(
                        user=request.user,
                        step__career=career,
                        completed=True
                    ).values_list('step_id', flat=True)
                )

                steps_data = []
                for i, step in enumerate(steps):
                    available = i == 0 or steps[i-1].id in completed_ids
                    steps_data.append({
                        'id': step.id,
                        'title': step.title,
                        'order_num': step.order_num,
                        'description': step.description,
                        'completed': step.id in completed_ids,
                        'available': available,
                    })

                return Response({
                    'career_id': career.id,
                    'career_title': career.title,
                    'category': career.category.title if career.category else '',
                    'steps': steps_data,
                })
            else:
                return Response({'career': None, 'message': 'Курс не выбран'})
        except Profile.DoesNotExist:
            return Response({'career': None, 'message': 'Курс не выбран'})
class CareerTestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("ПРИШЛО:", request.data)
        answer_ids = request.data.get('answers', [])

        if not answer_ids:
            return Response({'error':'Нет ответов'}, status=status.HTTP_400_BAD_REQUEST)
        
        answers = Answer.objects.filter(id__in=answer_ids).select_related('career')

        votes = Counter()

        for answer in answers:
            if answer.career:
                votes[answer.career.title] += 1
        
        if not votes:
            return Response({'message': 'Не удалось определить направление'})

        winner = votes.most_common(1)[0]

        return Response({
            'recommended': winner[0],
            'votes': winner[1],
            'all_votes': dict(votes),
        })

class CareerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Career.objects.prefetch_related('steps__materials').all()
    serializer_class = CareerSerializer
    search_fields = ['title', 'description', 'steps__title', 'steps__materials__title'  ]
    filterset_fields = ['category']

class StepViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Step.objects.prefetch_related('materials').all()
    serializer_class = StepSerializer

class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class MyProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress = Progress.objects.filter(user=request.user)
        serializer = ProgressSerializer(progress, many=True)
        return Response(serializer.data)

class MarkStepView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, step_id):
        try:
            step = Step.objects.get(id=step_id)
        except Step.DoesNotExist:
            return Response({'error': 'Шаг не найден'}, status=status.HTTP_404_NOT_FOUND)

        completed = request.data.get('completed', True)
        
        progress, created = Progress.objects.get_or_create(
            user=request.user,
            step = step,
        )
        progress.completed = completed
        progress.save()

        return Response({
            'message': f'Шаг "{step.title}" обновлён',
            'completed': progress.completed,
        })


class RegisterView(APIView):
    permission_classes = [AllowAny]
     
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Регистрация успешна',
                'username': serializer.data['username'],
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CareerProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, career_id):
        try:
            career = Career.objects.get(id=career_id)
        except Career.DoesNotExist:
            return Response({'error': 'Направление не найдено'}, status=status.HTTP_404_NOT_FOUND)

        total_steps = career.steps.count()

        completes_steps = Progress.objects.filter(
            user=request.user,
            step__career=career,
            completed=True,
        ).count()

        if total_steps > 0: 
            percent = round(completes_steps / total_steps * 100)
        else:
            percent = 0

        return Response({
            'career':career.title,
            'total_steps': total_steps,
            'completes_steps': completes_steps,
            'percent': percent,
        })