from rest_framework import viewsets
from .models import Career, Step, Material, Progress
from .serializers import CareerSerializer, StepSerializer, MaterialSerializer, ProgressSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
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