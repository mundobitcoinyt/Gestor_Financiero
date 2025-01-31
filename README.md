# Gestor_Financiero

Este es un gestor Financiero hecho en Python usando consejos de IA

A continuación te explicó un poco los pasos para hacerla funcionar.

1. En la carpeta data tendremos: data/budget.csv "aquí están todas los presupuestos agregados para cada categoría, podemos agregar mas desde aquí o desde la web".

2. En la misma carpeta date también tenemos:  data/transactions.csv "Desde acá se agregan las transacciones de ingresos y gastos" y usando los parámetros "Fecha,Monto,Tipo,Categoría".

3. Es necesario tener instaladas todas las dependencias o librerias que tenemos en el archivo" requirements.txt (Estos se pueden instalar desde la terminal usando esta linea de comando: "pip install -r requirements.txt" o "pip3 install -r requirements.txt" (sin las comillas)
   - Si hay errores con prophet, instala primero CMake usando: "pip install cmake" o a su vez "pip3 install cmake"

4. Para ejecutar la app en la web, usa la terminal de VS Code y ejecuta este código: streamlit run app.py
