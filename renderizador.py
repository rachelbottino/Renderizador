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

import math

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

    nq = int(input('''\nDigite um numero para o Supersampling do Triangulo \n
        (Lembrando que por exemplo 5 gera 5**2 áreas dentro do pixel e só numeros inteiros são aceitos) \n'''))

    #Transforma a cor do formato X3D (0,1) para o do Framebuffer (0,255)
    r = color[0]*255
    g = color[1]*255
    b = color[2]*255

    #vertices
    x0 = vertices[0]
    y0 = vertices[1]
    x1 = vertices[2]
    y1 = vertices[3]
    x2 = vertices[4]
    y2 = vertices[5]

    def reta(xa, ya, xb, yb, x, y):
        a0 = (yb-ya)
        b0 = (xb-xa)
        c0 = (ya*(xb-xa)-xa*(yb-ya))
        return(a0*x - b0*y + c0)

    alt = 0
    comp = 0
    comp_pixel = 0.5
    for alt in range(gpu.GPU.height):
        for comp in range(gpu.GPU.width):
            #NO PIXEL
            porcent_pixel = 0
            p = 0
            q = 0
            #DIVIDINDO O PIXEL EM N PARTES:
            #nq = 5
            dx = 0
            dy = (1/(-nq*2))
            for i in range (0,nq,1):
                dx = -1/(nq*2)
                dy += 1/nq
                for j in range (0,nq,1):
                    dx += 1/nq
                    r0 = reta(x0,y0,x1,y1,comp+(dx),alt+(dy))
                    r1 = reta(x1,y1,x2,y2,comp+(dx),alt+(dy))
                    r2 = reta(x2,y2,x0,y0,comp+(dx),alt+(dy))
                    if(r0>=0 and r1>=0 and r2>=0):
                        porcent_pixel+= 1/(nq**2)
            if porcent_pixel > 0:
                print("PORCENTAGEM: ", porcent_pixel)
                gpu.GPU.set_pixel(comp, alt, r*porcent_pixel, g*porcent_pixel, b*porcent_pixel) # altera um pixel da imagem
                     

'''
            r0 = reta(x0,y0,x1,y1,comp+(0.25),alt+(0.25))
            r1 = reta(x1,y1,x2,y2,comp+(0.25),alt+(0.25))
            r2 = reta(x2,y2,x0,y0,comp+(0.25),alt+(0.25))
            if(r0>=0 and r1>=0 and r2>=0):
                porcent_pixel+= 0.25
            #SEGUNDO QUADRANTE
            r0 = reta(x0,y0,x1,y1,comp+(0.75),alt+(0.25))
            r1 = reta(x1,y1,x2,y2,comp+(0.75),alt+(0.25))
            r2 = reta(x2,y2,x0,y0,comp+(0.75),alt+(0.25))
            if(r0>=0 and r1>=0 and r2>=0):
                porcent_pixel+= 0.25
            #TERCEIRO QUADRANTE
            r0 = reta(x0,y0,x1,y1,comp+(0.25),alt+(0.75))
            r1 = reta(x1,y1,x2,y2,comp+(0.25),alt+(0.75))
            r2 = reta(x2,y2,x0,y0,comp+(0.25),alt+(0.75))
            if(r0>=0 and r1>=0 and r2>=0):
                porcent_pixel+= 0.25
            #SEGUNDO QUADRANTE
            r0 = reta(x0,y0,x1,y1,comp+(0.75),alt+(0.75))
            r1 = reta(x1,y1,x2,y2,comp+(0.75),alt+(0.75))
            r2 = reta(x2,y2,x0,y0,comp+(0.75),alt+(0.75))
            if(r0>=0 and r1>=0 and r2>=0):
                porcent_pixel+= 0.25

            if porcent_pixel > 0:
                gpu.GPU.set_pixel(comp, alt, r*porcent_pixel, g*porcent_pixel, b*porcent_pixel) # altera um pixel da imagem
'''
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
