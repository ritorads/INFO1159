% Declaración de predicados dinámicos
:- dynamic paquete/6.
:- dynamic ubicacion/6.

:- encoding(utf8).

% ubicacion(ID, Tipo, Carga, CapacidadPeso, CapacidadVolumen, CategoriaPeso)
ubicacion(abarrotes_1_1, abarrotes, 0, 50, 5000, pesado).
ubicacion(abarrotes_1_2, abarrotes, 0, 500, 5000, medio).
ubicacion(abarrotes_1_3, abarrotes, 0, 500, 5000, liviano).

ubicacion(abarrotes_2_1, abarrotes, 0, 500, 100000, pesado).
ubicacion(abarrotes_2_2, abarrotes, 0, 500, 100000, medio).
ubicacion(abarrotes_2_3, abarrotes, 0, 500, 100000, liviano).

ubicacion(bebidas_1_1, bebidas, 0, 300, 80000, pesado).
ubicacion(bebidas_1_2, bebidas, 0, 300, 80000, medio).
ubicacion(bebidas_1_3, bebidas, 0, 300, 80000, liviano).

ubicacion(limpieza_1_1, limpieza, 0, 700, 150000, pesado).
ubicacion(limpieza_1_2, limpieza, 0, 700, 150000, medio).
ubicacion(limpieza_1_3, limpieza, 0, 700, 150000, liviano).

ubicacion(estmermas, mermas, 0, 500, 20000, ninguno).

% incompatibles(Categoria1, Categoria2)
incompatibles(abarrotes, limpieza).
incompatibles(bebidas, limpieza).
incompatibles(bebidas, abarrotes).

% paquete(ID, Peso, Dimensiones, Categoria, FechaExpiracion, UbicacionActual)
paquete('arroz', 5, (30, 20, 10), abarrotes, '15-11-2024', sin_ubicar).
paquete('tallarines', 52, (30, 20, 10), abarrotes, '15-11-2024', sin_ubicar).
paquete('galletas', 80, (55, 35, 15), abarrotes, '10-10-2024', sin_ubicar).
paquete('azucar', 10, (2, 20, 2), abarrotes, '20-12-2024', sin_ubicar).
paquete('aceite', 52, (50, 30, 30), abarrotes, '25-12-2024', sin_ubicar).
paquete('leche', 12, (20, 20, 30), abarrotes, '05-01-2025', sin_ubicar).
paquete('agua', 2, (10, 10, 30), bebidas, '01-12-2024', sin_ubicar).
paquete('gaseosa', 3, (15, 15, 35), bebidas, '20-12-2024', sin_ubicar).
paquete('jugo', 4, (20, 20, 25), bebidas, '30-11-2024', sin_ubicar).
paquete('jabon', 51, (10, 10, 10), limpieza, '15-10-2024', sin_ubicar).
paquete('cloro', 8, (25, 25, 40), limpieza, '25-12-2024', sin_ubicar).
paquete('detergente', 7, (30, 20, 20), limpieza, '10-01-2025', sin_ubicar).

% Reglas
ubicacionActual(ID, Ubicacion) :-
    paquete(ID, _, _, _, _, Ubicacion).

fechaEntero(Fecha, Numero) :-
    split_string(Fecha, "-", "", [DiaStr, MesStr, AnioStr]),
    number_string(Dia, DiaStr),
    number_string(Mes, MesStr),
    number_string(Anio, AnioStr),
    Numero is Anio * 10000 + Mes * 100 + Dia.

volumenPaquete(ID, Volumen) :-
    paquete(ID, _, (Ancho, Alto, Profundidad), _, _, _),
    Volumen is Ancho * Alto * Profundidad.

fechaActual(Fecha) :-
    get_time(Timestamp),
    stamp_date_time(Timestamp, DateTime, 'UTC'),
    format_time(atom(Fecha), '%d-%m-%Y', DateTime).

% Verificación de compatibilidad
sonCompatibles(Cat1, Cat2) :- 
    \+ incompatibles(Cat1, Cat2),
    \+ incompatibles(Cat2, Cat1).

actualizacionUbicacion(ID, NuevaUbicacion) :-
    paquete(ID, Peso, Dimensiones, Categoria, FechaExpiracion, UbicacionActual),
    retract(paquete(ID, Peso, Dimensiones, Categoria, FechaExpiracion, UbicacionActual)),
    assert(paquete(ID, Peso, Dimensiones, Categoria, FechaExpiracion, NuevaUbicacion)),

    % Si la ubicación actual no es 'sin_ubicar', actualiza la carga
    (UbicacionActual \= sin_ubicar ->
        retract(ubicacion(UbicacionActual, Categoria, CargaActual, CapacidadPesoActual, CapacidadVolumenActual, CategoriaPesoActual)),
        CargaNuevaActual is CargaActual - Peso,
        assert(ubicacion(UbicacionActual, Categoria, CargaNuevaActual, CapacidadPesoActual, CapacidadVolumenActual, CategoriaPesoActual))
    ; true),

    % Si la nueva ubicación no es 'sin_ubicar' ni 'estmermas', actualiza la carga
    (NuevaUbicacion \= sin_ubicar, NuevaUbicacion \= estmermas ->
        retract(ubicacion(NuevaUbicacion, Categoria, CargaNueva, CapacidadPesoNueva, CapacidadVolumenNueva, CategoriaPesoEstante)),
        CargaActualNueva is CargaNueva + Peso,
        assert(ubicacion(NuevaUbicacion, Categoria, CargaActualNueva, CapacidadPesoNueva, CapacidadVolumenNueva, CategoriaPesoEstante))
    ; true).


% Comprobar Vencimiento 
esVencido(ID) :-
    paquete(ID, _, _, _, FechaExpiracion, _),
    fechaActual(FechaActual),
    fechaEntero(FechaActual, FechaActualEntero),
    fechaEntero(FechaExpiracion, FechaExpir),
    FechaActualEntero >= FechaExpir.

manejarVencimiento(ID) :-
    (   esVencido(ID) ->
            write('El paquete '), write(ID), write(' ha expirado y se enviará a la ubicación de mermas.'), nl,
            actualizacionUbicacion(ID, estmermas)
        ;
            write('El paquete '), write(ID), write(' no ha expirado.'), nl
    ).

% Clasificar el peso de un paquete
clasificarPeso(Peso, CategoriaPeso) :-
    (   Peso =< 5
    ->  CategoriaPeso = liviano
    ;   
        Peso =< 50
    ->  CategoriaPeso = medio
    ;   
        CategoriaPeso = pesado).

% Verificar si hay suficiente peso disponible en una ubicación
pesoDisponible(Ubicacion, PesoDisp) :-
    ubicacion(Ubicacion, _, Carga, CapacidadPeso, _, _),
    PesoDisp is CapacidadPeso - Carga.

% Verificar si hay suficiente volumen disponible en una ubicación
volumenDisponible(Ubicacion, VolumenDisponible) :-
    ubicacion(Ubicacion, _, _, _, CapacidadVolumen, _),
    findall(Volumen, (
        paquete(_, _, (Ancho, Alto, Profundidad), _, _, Ubicacion), 
        Volumen is Ancho * Alto * Profundidad
    ), Volumenes),
    sum_list(Volumenes, VolumenOcupado),
    VolumenDisponible is CapacidadVolumen - VolumenOcupado.

% Asignar ubicación
asignarUbicacion(ID) :-
    paquete(ID, Peso, Dimensiones, CategoriaPaq, FechaExpiracion, sin_ubicar),
    nl, write('Asignando ubicación al paquete '), write(ID), nl,

    manejarVencimiento(ID),
    (   \+ esVencido(ID) ->
            clasificarPeso(Peso, CategoriaPeso),            
            % Buscar ubicaciones compatibles
            findall(Ubicacion, (
                ubicacion(Ubicacion, Categoria, _, _, _, CategoriaPesoEstante),
                sonCompatibles(CategoriaPaq, Categoria),
                CategoriaPesoEstante = CategoriaPeso
            ), UbicacionesCompatibles),
            
            % Ordenar las ubicaciones compatibles
            sort(UbicacionesCompatibles, UbicacionesCompatiblesOrdenadas),

            % Filtrar las ubicaciones que cumplen con los requisitos de capacidad
            include(cumpleRequisitos(Peso, Dimensiones), UbicacionesCompatiblesOrdenadas, UbicacionesDisponibles),
            
            (   
                UbicacionesDisponibles \= [] ->
                    % Si hay ubicaciones disponibles, asignar al primero de la lista
                    UbicacionesDisponibles = [PrimeraUbicacion | _],
                    actualizacionUbicacion(ID, PrimeraUbicacion),
                    write('El paquete '), write(ID), write(' ha sido asignado a la ubicación '), write(PrimeraUbicacion), nl
                ;
                    write('No hay ubicaciones disponibles para el paquete '), write(ID), nl
            )
        ;   
            true
    ).

cumpleRequisitos(Peso, (Ancho, Alto, Profundidad), Ubicacion) :-
    pesoDisponible(Ubicacion, PesoDisponible),
    Peso =< PesoDisponible,
    volumenDisponible(Ubicacion, VolumenDisponible),
    Volumen is Ancho * Alto * Profundidad,
    Volumen =< VolumenDisponible.

/* Asignar todos los paquetes sin ubicar */
asignar_todos_paquetes :-
    findall(ID, paquete(ID, _, _, _, _, sin_ubicar), Paquetes),
    forall(member(ID, Paquetes), asignarUbicacion(ID)).

% Mostrar detalles de todos los estantes
mostrarDetallesEstantes :-
    % Obtener todas las ubicaciones en una lista
    findall((Ubicacion, Categoria, Carga, CapacidadPeso, CapacidadVolumen, CategoriaPeso),
            ubicacion(Ubicacion, Categoria, Carga, CapacidadPeso, CapacidadVolumen, CategoriaPeso),
            Ubicaciones),
    
    % Ordenar las ubicaciones
    sort(Ubicaciones, UbicacionesOrdenadas),
    
    % Imprimir los detalles de cada estante en forma ordenada
    forall(member((Ubicacion, Categoria, Carga, CapacidadPeso, CapacidadVolumen, CategoriaPeso), UbicacionesOrdenadas), (
        pesoDisponible(Ubicacion, PesoDisp),
        volumenDisponible(Ubicacion, VolumenDisp),
        write('Ubicación: '), write(Ubicacion), nl,
        write('Carga Actual: '), write(Carga), write('/'), write(CapacidadPeso), write(' kg'), nl,
        write('Volumen Disponible: '), write(VolumenDisp), write('/'), write(CapacidadVolumen), write(' cm³'), nl,
        write('Categoría de peso: '), write(CategoriaPeso), nl, nl
    )).
