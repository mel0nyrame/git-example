3#include<stdio.h>
int main()
{
	int N;
	scanf("%d",&N);
	int n=N;
	int min=1;
	int max=10;
	while(N>1){
		N--;
		min*=10;
		max*=10;
		//printf("min=%d\n",min);
		//printf("max=%d\n",max);
	}
	int i=min;
	while(i<max){
		int sum=0;
		int t=i;
		do{
			int d=t%10;
			t/10;
			int p=d;
			int j=1;
			while(j<N){
				p*=d;
				j++;
				sum+=p;
				}
			if(sum==i){
			printf("%d",sum);
			} 
		} while(t>0);
		i++;
	}
	return 0;
}
