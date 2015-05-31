/*
 * A topological sorting implementation by James Swineson.
 * http://swineson.me
 * 2015-06-01
 * 
 * ** THIS PROGRAM IS NOT FULLY TESTED AND USE AT YOUR OWN RISK!!! **
 *
 * License
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */
 
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

// ===============================================
// 一个简单的二维数组实现

#define ARRAY_ELEMENT_TYPE int
#define ARRAY_ELEMENT_DEFAULT_VALUE 0

// 二维数组结构体
typedef struct struct_2dArray {
	ARRAY_ELEMENT_TYPE **data;		// 数组元素值
	int dimX;						// 第一个下标最大值
	int dimY;						// 第二个下标最大值
} s2dArray;

// 创建二维数组
s2dArray *malloc2dArray(int dimX, int dimY) {
	// 分配第一层
	ARRAY_ELEMENT_TYPE **arr = malloc(dimX * sizeof(ARRAY_ELEMENT_TYPE *));
	if(arr == NULL) {
	    fprintf(stderr, "There is not enough memory.\n");
	    exit (EXIT_FAILURE);
	}
	// 分配第二层
	for(int i = 0; i < dimX; i++) {
	    arr[i] = malloc(dimY * sizeof(ARRAY_ELEMENT_TYPE)); 
		if(arr[i] == NULL) { 
		    fprintf(stderr, "There is not enough memory.\n");
		    exit (EXIT_FAILURE);        
		}
	}
	// 写入结构体
	s2dArray *a = malloc(sizeof(s2dArray));
	a->data = arr;
	a->dimX = dimX;
	a->dimY = dimY;
	return a;
}

// 释放二维数组
void free2dArray(s2dArray *arr) {
	for(int i = 0; i < arr->dimX; i++)
		free(arr->data[i]);
	free(arr->data);
	free(arr);
}

// 获取某个位置的元素值
ARRAY_ELEMENT_TYPE getValueOf2dArray(s2dArray *arr, int X, int Y) {
	if (X >= arr->dimX || Y >= arr->dimY) return ARRAY_ELEMENT_DEFAULT_VALUE;
	return arr->data[X][Y];
}

// 写入某个位置的元素值
ARRAY_ELEMENT_TYPE setValueOf2dArray(s2dArray *arr, int X, int Y, ARRAY_ELEMENT_TYPE newValue) {
	if (X >= arr->dimX || Y >= arr->dimY) return ARRAY_ELEMENT_DEFAULT_VALUE;
	return (arr->data[X][Y] = newValue);
}

// 以一维数组形式获取某一列
ARRAY_ELEMENT_TYPE *getDimXValueAsArray(s2dArray *arr, int dimY) {
	ARRAY_ELEMENT_TYPE *d = malloc(arr->dimX * sizeof(ARRAY_ELEMENT_TYPE));
	for (int i = 0; i < arr->dimX; i++)
		d[i] = getValueOf2dArray(arr, i, dimY);
	return d;
}

// 以一维数组形式获取某一行
ARRAY_ELEMENT_TYPE *getDimYValueAsArray(s2dArray *arr, int dimX) {
	ARRAY_ELEMENT_TYPE *d = malloc(arr->dimY * sizeof(ARRAY_ELEMENT_TYPE));
	for (int i = 0; i < arr->dimY; i++)
		d[i] = getValueOf2dArray(arr, dimX, i);
	return d;
}

// 设置某一列为统一值
void setDimXValueOf2dArray(s2dArray *arr, int dimY, ARRAY_ELEMENT_TYPE value) {
	for (int i = 0; i < arr->dimX; i++)
		setValueOf2dArray(arr, i, dimY, value);
}

// 设置某一行为统一值
void setDimYValueOf2dArray(s2dArray *arr, int dimX, ARRAY_ELEMENT_TYPE value) {
	for (int i = 0; i < arr->dimY; i++)
		setValueOf2dArray(arr, dimX, i, value);
}

// 整个数组内容填充为统一值
void fill2dArray(s2dArray *arr, ARRAY_ELEMENT_TYPE value) {
	for (int i = 0; i < arr->dimX; i++)
		for (int j = 0; j < arr->dimY; j++)
			setValueOf2dArray(arr, i, j, value);
}

// ===============================================
// 一维数组相关操作

// 建立一个一维数组并且所有元素置零
void *mallocArrayAndFillZero(size_t size) {
	void *a = malloc(size);
	memset(a, 0, size);
	return a;
}

// 求数组元素和
ARRAY_ELEMENT_TYPE sumOfArray(ARRAY_ELEMENT_TYPE *arr, int length) {
	ARRAY_ELEMENT_TYPE sum = 0;
	for (int i = 0; i < length; i++) sum += arr[i];
	return sum;
}

// ===============================================
// 如何优雅地使用邻接矩阵

// 分配内存空间
s2dArray *mallocAdjacencyMatrix(int n) {
	return malloc2dArray(n, n);
}

// 获取列向量
int *getColumnArray(s2dArray *arr, int row) {
	int *col = getDimXValueAsArray(arr, row);
	return col;
}

// 求入度（列向量求和）
int getInDegree(s2dArray *arr, int row) {
	int *a = getColumnArray(arr, row);
	int s = sumOfArray(a, arr->dimX);
	free(a);
	return s;
}

// 行向量置零
void fillZeroInColumn(s2dArray *arr, int col) {
	setDimYValueOf2dArray(arr, col, 0);
}

// ===============================================
// 有向图相关操作

// 找到下一个需要输出的顶点并返回其序号；找不到下一个时返回 -1
int findNextPoint(s2dArray *mat) {
	int n = mat->dimX;
	static bool *hasFound = NULL;
	if (hasFound == NULL) hasFound = mallocArrayAndFillZero(n * sizeof(bool));
	int scanptr = 0;
	while (scanptr < n && hasFound[scanptr] && !getInDegree(mat, scanptr)) scanptr++;
	if (scanptr < n) {
		// 找到新的点
		hasFound[scanptr] = true;			// 删除该顶点
		fillZeroInColumn(mat, scanptr);		// 删除以该顶点为尾的弧
		return scanptr;
	} else {
		// 所有点都已经输出，查找结束
		free(hasFound);
		hasFound = NULL;
		return -1;
	}
}

// ===============================================
// 终于看到主程序了好开心

int main(void) {
	int n;
	printf("Total points count: ");
	scanf("%d", &n);
	
	s2dArray *mat = mallocAdjacencyMatrix(n);
	// 其实这里就是输入 n 个数
	printf("Adjacency matrix of %d by %d:\n", n, n);
	for (int i = 0; i < n*n; i++) {
		int next_input;
		scanf("%d", &next_input);
		setValueOf2dArray(mat, i/n, i%n, next_input);
	}
	
	int next_point;
	printf("\nSequence: ");
	while ((next_point = findNextPoint(mat)) != -1) {
		printf("%d ", next_point + 1);
	}
	puts("");
	
	free2dArray(mat);
	
	return 0;
}