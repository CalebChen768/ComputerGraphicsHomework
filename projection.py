import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  

def homo2cart(points):
    '''将齐次坐标转换为笛卡尔坐标'''
    points=points[:,:-1]/points[:,-1:]
    return points

def projection_trans(view_point,points):
    '''获得投影变换之后的点阵'''
    x0,y0,z0 = view_point[0],view_point[1],view_point[2]
    d=-1*z0
    mtx=np.array([[1,0,0,0],
                [0,1,0,0],
                [x0/d,y0/d,0,1/d],
                [0,0,0,1]],dtype=np.float32)
    print(mtx)
    new_points=np.matmul(points,mtx)
    return new_points

def one_point_projection(L,M,N,view_point,point):
    '''一点'''
    mtx_mv=np.array([[1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [L,M,N,1]],dtype=np.float32)
    point=np.matmul(point,mtx_mv)
   # print(point)
    new_point=projection_trans(view_point,point)
    return new_point,point

def two_point_projection(L,M,N,a,view_point,point):
    '''二点'''
    #先移动L，M，N
    mtx_mv=np.array([[1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [L,M,N,1]],dtype=np.float32)
    point=np.matmul(point,mtx_mv)

    #绕y轴旋转 a 度（a<90deg）
    a=a/180*np.pi
    mtx_roty=np.array([[np.cos(a),0,np.sin(a),0],
                    [0,1,0,0],
                    [-1*np.sin(a),0,np.cos(a),0],
                    [0,0,0,1]],dtype=np.float32)
    point=np.matmul(point,mtx_roty)

   # print(point)
    new_point=projection_trans(view_point,point)
    return new_point,point


def three_point_projection(L,M,N,a,b,view_point,point):
    '''三点'''
    #先移动L，M，N
    mtx_mv=np.array([[1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [L,M,N,1]],dtype=np.float32)
    point=np.matmul(point,mtx_mv)
    print("aaa")
    print(point)
    #绕y轴旋转 a 度（a<90deg）
    a=a/180*np.pi
    mtx_roty=np.array([[np.cos(a),0,np.sin(a),0],
                    [0,1,0,0],
                    [-1*np.sin(a),0,np.cos(a),0],
                    [0,0,0,1]],dtype=np.float32)
    point=np.matmul(point,mtx_roty)
    print("bbb")
    print(point)
    #绕x轴旋转 b 度（b<90deg）
    b=b/180*np.pi
    mtx_rotx=np.array([[1,0,0,0],
                    [0,np.cos(b),np.sin(b),0],   
                    [0,-1*np.sin(b),np.cos(b),0],
                    [0,0,0,1]],dtype=np.float32)
    point=np.matmul(point,mtx_rotx)
    print("ccc")
    print(point)
   # print(point)
    new_point=projection_trans(view_point,point)
    return new_point,point


view_point = np.array([0,0,-1,1],dtype=np.float32)
points= np.array([[0,0,0,1],
                [1,0,0,1],
                [1,1,0,1],
                [0,1,0,1],
                [0,0,0,1],
                [0,0,1,1],
                [1,0,1,1],
                [1,1,1,1],
                [0,1,1,1],
                [0,0,1,1],
                [0,0,0,1],
                [1,0,0,1],
                [1,0,1,1],
                [1,1,1,1],
                [1,1,0,1],
                [0,1,0,1],
                [0,1,1,1]],dtype=np.float32)
               

#new_points=one_point_projection(0,0,0,view_point,points)
new_points,ori_points=three_point_projection(2,3,1,50,30,view_point,points)

new_points=homo2cart(new_points)


def draw(view_point,ori_points,new_points):
    plt.scatter(new_points[:,0],new_points[:,1],c="black")
    plt.plot(new_points[:,0],new_points[:,1],c="black")
    ax=Axes3D(plt.figure())

    x = np.linspace(-6,6,100)
    y = np.linspace(-6,6,100)
    X, Y = np.meshgrid(x, y)


    ax.plot_surface(X,Y,Z=X*0,color='g',alpha=0.3) 

    ax.scatter(ori_points[:,0],ori_points[:,1],ori_points[:,2])
    ax.scatter(view_point[0],view_point[1],view_point[2],c='r')
    ax.plot(ori_points[:,0],ori_points[:,1],ori_points[:,2])
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1,1, 0.5, 1]))

    ax.scatter(new_points[:,0],new_points[:,1],c="black")
    ax.plot(new_points[:,0],new_points[:,1],c="black")


    ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'red'})
    ax.set_xlabel('X', fontdict={'size': 15, 'color': 'red'})



    plt.show()



draw(view_point,ori_points,new_points)