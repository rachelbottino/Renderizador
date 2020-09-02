# Desenvolvido por: Luciano Soares
# Displina: Computação Gráfica
# Data: 28 de Agosto de 2020

import argparse

# X3D
import x3d

# Interface
import interface

# GPU
import gpu

def polypoint2D(point, color):
    """ Função usada para renderizar Polypoint2D. """
    print("Pontos: ", point, color)
    #Transforma a cor do formato X3D (0,1) para o do Framebuffer (0,255)
    c0 = color[0]*255
    c1 = color[1]*255
    c2 = color[2]*255
    i = 0
    while (i < len(point)):
        x = int(point[i])
        y = int(point[i+1])
        
        print("Ponto: ", x, y, " Cor: ", c0, c1, c2)
        gpu.GPU.set_pixel(x, y, c0, c1, c2)

        i+=2

    #gpu.GPU.set_pixel(3, 1, c0, c1, c2) # altera um pixel da imagem
    # cuidado com as cores, o X3D especifica de (0,1) e o Framebuffer de (0,255)

def polyline2D(lineSegments, color):
    """ Função usada para renderizar Polyline2D. """

    #Transforma a cor do formato X3D (0,1) para o do Framebuffer (0,255)
    c0 = color[0]*255
    c1 = color[1]*255
    c2 = color[2]*255
    
    #Pontos 0 e 1 no segmento
    x0 = lineSegments[0]
    y0 = lineSegments[1]
    x1 = lineSegments[2]
    y1 = lineSegments[3]

    print("Linha: ", x0, y0, x1, y1, "Cor: ", c0, c1, c2)

    #inclinação da linha
    #s = (y1-y0)/((x1-x0)*y0)
    #print("Inclinacao: ", s)

    def plotLineLow(x0,y0,x1,y1):        
        dx = x1-x0
        dy = y1-y0
        yi = 1
        if dy < 0:
            yi  = -1
            dy = -dy
        d = 2*dy - dx
        x = x0
        y = y0
        while (x < x1 and abs(y) < gpu.GPU.height and abs(x) < gpu.GPU.width):
            gpu.GPU.set_pixel(int(x), int(y), c0, c1, c2) # altera um pixel da imagem
            if d > 0:
                y = y+yi
                d = d - 2*dx
            d = d+2*dy      
            x+=1

    def plotLineHigh(x0,y0,x1,y1):
        dx = x1-x0
        dy = y1-y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx
        d = 2*dx - dy
        x = x0
        y = y0
        while (y < y1 and y < gpu.GPU.height and x < gpu.GPU.width):
            gpu.GPU.set_pixel(int(x), int(y), c0, c1, c2) # altera um pixel da imagem
            if d > 0:
                x = x+xi
                d = d - 2*dy
            d = d+2*dx       
            y+=1

    def plotLine(x0,y0,x1,y1):
        if(abs(y1-y0) < abs(x1-x0)):
            if x0 > x1:
                plotLineLow(x1,y1,x0,y0)
            else:
                plotLineLow(x0,y0,x1,y1)
        else:
            if y0 > y1:
                plotLineHigh(x1,y1,x0,y0)
            else:
                plotLineHigh(x0,y0,x1,y1)

    plotLine(x0,y0,x1,y1)
    
def triangleSet2D(vertices, color):
    """ Função usada para renderizar TriangleSet2D. """

    #Transforma a cor do formato X3D (0,1) para o do Framebuffer (0,255)
    c0 = color[0]*255
    c1 = color[1]*255
    c2 = color[2]*255

    #vertices
    x0 = vertices[0]
    y0 = vertices[1]
    x1 = vertices[2]
    y1 = vertices[3]
    x2 = vertices[4]
    y2 = vertices[5]

    a0 = (y0-y1)
    b0 = (x1-x0)
    #c0 = y0*(x1-x0) - x0*(y1-y0)
    c0 = (x0*x1 - (x1*y0))

    a1 = (y1-y2)
    b1 = (x2-x1)
    #c1 = y1*(x2-x1) - x1*(y2-y1)
    c1 = (x1*y2 - (x2*y1))

    a2 = (y2-y0)
    b2 = (x0-x2)
    #c2 = y2*(x0-x2) - x2*(y0-y2)
    c2 = (x2*y0 - (x0*y2))
    print("EQUACAO:", a0,"*COMP",b0,"*alt+",c0 )
    print("EQUACAO:", a1,"*COMP",b1,"*alt+",c1 )
    print("EQUACAO:", a2,"*COMP",b2,"*alt+",c2 )
    
    alt = 0
    comp = 0
    for alt in range(gpu.GPU.height):
        for comp in range(gpu.GPU.width):
            print(comp, alt)
            r0 = a0*comp + b0*alt + c0
            r1 = a1*comp + b1*alt + c1
            r2 = a2*comp + b2*alt + c2
            print(r0,r1,r2)
            if(r0<=0 and r1<=0 and r2<=0):
                print("DENTRO DO TRIANGULO")
                print("PIXEL ",comp,",",alt)
                gpu.GPU.set_pixel(comp, alt, c0, c1, c2) # altera um pixel da imagem

LARGURA = 30
ALTURA = 20

if __name__ == '__main__':
    
    width = LARGURA
    height = ALTURA
    x3d_file = "exemplo1.x3d"
    image_file = "tela.png"

    # Tratando entrada de parâmetro
    parser = argparse.ArgumentParser(add_help=False)   # parser para linha de comando
    parser.add_argument("-i", "--input", help="arquivo X3D de entrada")
    parser.add_argument("-o", "--output", help="arquivo 2D de saída (imagem)")
    parser.add_argument("-w", "--width", help="resolução horizonta", type=int)
    parser.add_argument("-h", "--height", help="resolução vertical", type=int)
    args = parser.parse_args() # parse the arguments
    if args.input: x3d_file = args.input
    if args.output: image_file = args.output
    if args.width: width = args.width
    if args.height: height = args.height
    
    # Iniciando simulação de GPU
    gpu.GPU(width, height)

    # Abre arquivo X3D
    scene = x3d.X3D(x3d_file)
    scene.set_resolution(width, height)

    # funções que irão fazer o rendering
    x3d.X3D.render["Polypoint2D"] = polypoint2D
    x3d.X3D.render["Polyline2D"] = polyline2D
    x3d.X3D.render["TriangleSet2D"] = triangleSet2D

    scene.parse() # faz o traversal no grafo de cena
    interface.Interface(width, height, image_file).preview(gpu.GPU._frame_buffer)
