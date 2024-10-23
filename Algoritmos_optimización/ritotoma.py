def No_Negatividad(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} no puede ser negativo")
    return ivalue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algoritmo genético")
    parser.add_argument("--generaciones", type=No_Negatividad, help="Cantidad de generaciones máximas", required=True)
    parser.add_argument("--individuos", type=No_Negatividad, help="Cantidad de individuos", required=True)
    parser.add_argument("--movimientos", type=No_Negatividad, help="Cantidad de movimientos", required=True)
    parser.add_argument("--probabilidad", type=float, help="Probabilidad de asesino", required=True)
    parser.add_argument("--mutacion", type=float, help="Probabilidad de mutación", required=True)
    parser.add_argument("--iteraciones", type=No_Negatividad, help="Cantidad de iteraciones", required=True)
    parser.add_argument("--opciones", type=str, help="Opciones 'Si' o 'No'", choices=["Si", "No"], required=True)

    args = parser.parse_args()
    print(args.probabilidad)

    funcionamiento_principal(
        args.generaciones,
        args.individuos,
        args.movimientos,
        args.probabilidad,
        args.mutacion,
        #args.iteraciones,
        #args.opciones
        )
