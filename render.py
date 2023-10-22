import matplotlib.pyplot as plt

# Algoritmo de Bresenham
def bresenham_algorithm(x0, y0, x1, y1):
    line_pixels = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy

    # Loop para definir los pixeles que conforman la línea
    # a partir de los vertices de inicio y final
    while x0 != x1 or y0 != y1:
        line_pixels.append((x0, y0))
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return line_pixels

def interpolate_color(color1, color2, t):
    r = color1[0] * (1 - t) + color2[0] * t
    g = color1[1] * (1 - t) + color2[1] * t
    b = color1[2] * (1 - t) + color2[2] * t
    return r, g, b

def interpolate(line_pixels, color_a, color_b, ax, square_size):
    for i, pixel in enumerate(line_pixels):
        # Conocer la cantidad de pasos para blendear el color
        t = i / len(line_pixels)
        # Aplicar interpolación
        blended_color = interpolate_color(color_a, color_b, t)
        # Dar color al pixel
        ax.add_patch(plt.Rectangle((pixel[0], pixel[1]), square_size, square_size, fill=True, color=blended_color))
        #ax.plot(pixel[0] + 0.5, pixel[1] + 0.5, 'go')

def draw_grid_with_vertices_and_edges(vertices, edges, num_rows=24, num_cols=24, square_size=1):
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    # Dibujar la grid de cuadrados (pixeles de la pantalla)
    for i in range(num_rows):
        for j in range(num_cols):
            rect = plt.Rectangle((i, j), square_size, square_size, fill=None, edgecolor='black')
            ax.add_patch(rect)

    # Dibujar los vertices en el pixel correspondiente (solo para visualizar)
    for vertex in vertices:
        color = [val / 255 for val in vertex[2]]
        ax.add_patch(plt.Rectangle((vertex[0], vertex[1]), square_size, square_size, fill=True, color=color))
        ax.plot(vertex[0]+0.5, vertex[1]+0.5, 'wo')

    # Aplicar rasterización con Bresenham e Interpolación
    for i in range(0, len(edges), 4):   # Avanzar cada 4 edges

        # Se aplica loop unrolling en las siguientes secciones para visualizar
        # las partes que pueden ser vectorizadas

        # Dibujar edges con matplot (solo para visualizar la línea matemática)
        ax.plot([edges[i][0][0]+0.5, edges[i][1][0]+0.5], [edges[i][0][1]+0.5, edges[i][1][1]+0.5], color='black')
        ax.plot([edges[i+1][0][0]+0.5, edges[i+1][1][0]+0.5], [edges[i+1][0][1]+0.5, edges[i+1][1][1]+0.5], color='black')
        ax.plot([edges[i+2][0][0]+0.5, edges[i+2][1][0]+0.5], [edges[i+2][0][1]+0.5, edges[i+2][1][1]+0.5], color='black')
        ax.plot([edges[i+3][0][0]+0.5, edges[i+3][1][0]+0.5], [edges[i+3][0][1]+0.5, edges[i+3][1][1]+0.5], color='black')
        
        # Obtener los vertices que conforman el edge 
        v1, v2 = edges[i]
        v3, v4 = edges[i+1]
        v5, v6 = edges[i+2]
        v7, v8 = edges[i+3]

        # Aplicar Bresenham conociendo las coordenadas de los vertices
        # Acá cada cálculo de Bresenham puede ser paralelizado porque son 
        # cálculos independientes
        line_pixels_12 = bresenham_algorithm(v1[0], v1[1], v2[0], v2[1])
        line_pixels_34 = bresenham_algorithm(v3[0], v3[1], v4[0], v4[1])
        line_pixels_56 = bresenham_algorithm(v5[0], v5[1], v6[0], v6[1])
        line_pixels_78 = bresenham_algorithm(v7[0], v7[1], v8[0], v8[1])

        # Mapear los valores rgb de 0-1 (requisito solo de matplot)
        color1 = [val / 255 for val in v1[2]]
        color2 = [val / 255 for val in v2[2]]
        color3 = [val / 255 for val in v3[2]]
        color4 = [val / 255 for val in v4[2]]
        color5 = [val / 255 for val in v5[2]]
        color6 = [val / 255 for val in v6[2]]
        color7 = [val / 255 for val in v7[2]]
        color8 = [val / 255 for val in v8[2]]

        # Interpolación
        interpolate(line_pixels_12, color1, color2, ax, square_size)
        interpolate(line_pixels_34, color3, color4, ax, square_size)
        interpolate(line_pixels_56, color5, color6, ax, square_size)
        interpolate(line_pixels_78, color7, color8, ax, square_size)

    ax.set_xlim(0, num_rows)
    ax.set_ylim(0, num_cols)
    plt.show()

def main():
    # Definir los vertices que conforman la imagen
    # vertex = (x, y, (r, g, b))
    vertices = [(2,  1,  (255, 130, 89)), (2,  14, (40, 29, 60)), 
                (11, 21, (18,  69, 180)), (20, 14, (80, 225, 59)), 
                (21, 1,  (230, 0, 120))]
                
    # Definir los edges para unir los vertices
    # edge = (vertex_a, vertex_b)                
    edges = [(vertices[0], vertices[1]), (vertices[1], vertices[2]), 
             (vertices[2], vertices[3]), (vertices[3], vertices[4]),
             (vertices[4], vertices[1]), (vertices[0], vertices[4]),
             (vertices[0], vertices[3]), (vertices[1], vertices[3])]

    # Llamar a la función principal
    draw_grid_with_vertices_and_edges(vertices, edges)

if __name__ == '__main__':
    main()
