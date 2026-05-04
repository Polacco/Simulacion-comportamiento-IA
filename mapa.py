LUGARES = {
    "Entrada": (0, 10),
    "Escritorio Jorge": (1, 1),
    "Escritorio Juan": (3, 1),
    "Escritorio Lucas": (1, 10),
    "Escritorio Pedro": (10, 1),
    "Escritorio Julia": (10, 10),
    "Mesa de Reuniones": (6, 6),
    "Cafetera": (1, 5),
    "Baño": (10, 5),
    "Pizarra": (5, 1)
}

def obtener_descripcion_mapa():
    descripcion = "Mapa de la oficina (Grilla 12x12):\n"
    for lugar, coord in LUGARES.items():
        descripcion += f"- {lugar}: en coordenadas {coord}\n"
    return descripcion