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

def one_point_perspective(L,M,N,view_point,point):
    '''一点透视：移动L，M，N'''
    mtx_mv=np.array([[1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [L,M,N,1]],dtype=np.float32)
    new_point=np.matmul(point,mtx_mv)

    return new_point

def two_point_perspective(L,M,N,a,view_point,point):
    '''二点透视'''
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
    new_point=np.matmul(point,mtx_roty)

    return new_point


def three_point_perspective(L,M,N,a,b,view_point,point):
    '''三点透视'''
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

    #绕x轴旋转 b 度（b<90deg）
    b=b/180*np.pi
    mtx_rotx=np.array([[1,0,0,0],
                    [0,np.cos(b),np.sin(b),0],   
                    [0,-1*np.sin(b),np.cos(b),0],
                    [0,0,0,1]],dtype=np.float32)
    new_point=np.matmul(point,mtx_rotx)

    return new_point


def draw(view_point,ori_points,mv_points,new_points):
    plt.scatter(new_points[:,0],new_points[:,1],c="black")
    plt.plot(new_points[:,0],new_points[:,1],c="black")
    ax=Axes3D(plt.figure())

    x = np.linspace(-6,6,100)
    y = np.linspace(-6,6,100)
    X, Y = np.meshgrid(x, y)


    ax.plot_surface(X,Y,Z=X*0,color='g',alpha=0.3) 

    #原来的点阵
    ax.scatter(ori_points[:,0],ori_points[:,1],ori_points[:,2],c="brown")
    ax.plot(ori_points[:,0],ori_points[:,1],ori_points[:,2],c="brown")
    #透视移动后
    ax.scatter(mv_points[:,0],mv_points[:,1],mv_points[:,2])
    ax.scatter(view_point[0],view_point[1],view_point[2],c='r')
    ax.plot(mv_points[:,0],mv_points[:,1],mv_points[:,2])
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1,1, 1, 1]))
    #投影后
    ax.scatter(new_points[:,0],new_points[:,1],c="black")
    ax.plot(new_points[:,0],new_points[:,1],c="black")

    #原来与移动后点两两连接
    for i in range(len(mv_points)):
        ax.plot([ori_points[i,0],mv_points[i,0]],[ori_points[i,1],mv_points[i,1]],[ori_points[i,2],mv_points[i,2]],c="pink",linestyle='--')
    #两组点两两连接
    for i in range(len(mv_points)):
        ax.plot([mv_points[i,0],view_point[0]],[mv_points[i,1],view_point[1]],[mv_points[i,2],view_point[2]],c='y',linestyle='dashdot')

    ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'red'})
    ax.set_xlabel('X', fontdict={'size': 15, 'color': 'red'})

    plt.show()


#视点（0，0，-1，1）
view_point = np.array([4,4,-2,1],dtype=np.float32)
#以（0，0，0）为原点的正方体
points= np.array([[0,0,0,1],
                [2,0,0,1],
                [2,2,0,1],
                [0,2,0,1],
                [0,0,0,1],
                [0,0,2,1],
                [2,0,2,1],
                [2,2,2,1],
                [0,2,2,1],
                [0,0,2,1],
                [0,0,0,1],
                [2,0,0,1],
                [2,0,2,1],
                [2,2,2,1],
                [2,2,0,1],
                [0,2,0,1],
                [0,2,2,1]],dtype=np.float32)
                
#获得透视移动后的点和投影后的点
#per_points=one_point_perspective(6,5,1,view_point,points)
#per_points=two_point_perspective(3,3,2,60,view_point,points)
#透视移动后的点
per_points=three_point_perspective(3,3,2,60,60,view_point,points)
#投影后的点
pro_points=projection_trans(view_point,per_points)
#转为笛卡尔坐标系
per_points=homo2cart(per_points)
pro_points=homo2cart(pro_points)

#画图
draw(view_point,points,per_points,pro_points)