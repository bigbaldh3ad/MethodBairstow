from django.shortcuts import render
from .forms import BairstowForm
from .bairstow import bairstow, graficar_convergencia
import sympy as sp
import os
from .models import BairstowRegistro


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BairstowRegistroSerializer


def portada(request):
    return render(request, 'bairstow_app/portada.html')


def historial(request):
    registros = BairstowRegistro.objects.order_by('-fecha')
    return render(request, 'bairstow_app/historial.html', {'registros': registros})


def home(request):
    result = None
    steps = []
    grafica_url = None
    if request.method == 'POST':
        form = BairstowForm(request.POST)
        if form.is_valid():
            ecuacion = form.cleaned_data['ecuacion']
            r = form.cleaned_data['r']
            s = form.cleaned_data['s']
            tol = form.cleaned_data['tol']
            max_iter = form.cleaned_data['max_iter']

            x = sp.symbols('x')
            poly_expr = sp.sympify(ecuacion)
            coeffs = sp.Poly(poly_expr, x).all_coeffs()
            coeffs = [float(c) for c in coeffs]

            # Llamamos a la función bairstow para obtener las raíces y pasos
            result, steps = bairstow(coeffs, r, s, tol, max_iter)

            # Convertimos las raíces a flotantes y les damos un formato con 4 decimales
            if result:
                result = [str(root) if isinstance(root, complex) else round(float(root), 4) for root in result]

            if steps:
                static_path = os.path.join('bairstow_app', 'static', 'bairstow_app', 'graficas')
                filename = graficar_convergencia(steps, static_path)
                grafica_url = f'bairstow_app/graficas/{filename}'

            if result:
                BairstowRegistro.objects.create(
                    ecuacion=ecuacion,
                    r_inicial=r,
                    s_inicial=s,
                    tolerancia=tol,
                    max_iter=max_iter,
                    raices=str(result),  # Almacenar las raíces ya convertidas a formato legible
                    grafica=grafica_url if grafica_url else ''
                )
    else:
        form = BairstowForm()

    return render(request, 'bairstow_app/index.html', {
        'form': form,
        'result': result,
        'steps': steps,
        'grafica_url': grafica_url,
    })


class BairstowListAPI(APIView):
    def get(self, request):
        registros = BairstowRegistro.objects.all().order_by('-fecha')
        serializer = BairstowRegistroSerializer(registros, many=True)
        return Response(serializer.data)


class BairstowCreateAPI(APIView):
    def post(self, request):
        data = request.data
        try:
            ecuacion = data['ecuacion']
            r = float(data['r'])
            s = float(data['s'])
            tol = float(data['tolerancia'])
            max_iter = int(data['max_iter'])

            x = sp.symbols('x')
            poly_expr = sp.sympify(ecuacion)
            coeffs = sp.Poly(poly_expr, x).all_coeffs()
            coeffs = [float(c) for c in coeffs]

            result, steps = bairstow(coeffs, r, s, tol, max_iter)

            grafica_url = None
            if steps:
                static_path = os.path.join('bairstow_app', 'static', 'bairstow_app', 'graficas')
                filename = graficar_convergencia(steps, static_path)
                grafica_url = f'bairstow_app/graficas/{filename}'

            registro = BairstowRegistro.objects.create(
                ecuacion=ecuacion,
                r_inicial=r,
                s_inicial=s,
                tolerancia=tol,
                max_iter=max_iter,
                raices=str(result),
                grafica=grafica_url
            )

            serializer = BairstowRegistroSerializer(registro)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
