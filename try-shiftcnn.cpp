/*
 *        (C) COPYRIGHT Ingenic Limited.
 *             ALL RIGHTS RESERVED
 *
 * File       : try-shiftcnn.cpp
 * Authors    : ydwu@aries
 * Create Time: 2017-12-05:21:11:17
 * Description:
 * 
 */

#include <iostream>
#include <math.h>

using namespace std;

int main(int argc, char** argv)
{
  int N=2;
  int B=4;
  double weight_Q = 0;
  double weight = 0;
  cin >> weight;
  for(int n=0; n<N; n++)
    {
      cout << "+++++weight:" << weight << endl;
      float qSgn=1.0;
      if(weight<0)
	qSgn=-1.0;
      double qLog = log(fabs(weight))/log(2);
      cout << "+++++qLog:" << qLog << endl;
      double qIdx = floor(qLog);
      cout << "+++++qIdx:" << qIdx << endl;
      double bLog = qIdx + log(1.5)/log(2);
      cout << "+++++bLog:" << bLog << endl;
      if(qLog > bLog) // border condition
	qIdx++;
      cout << "+++++qIdx:" << qIdx << endl;
      double q = qSgn * pow(2,qIdx);
      double qIdxMem = qSgn * (-(n+1)-qIdx+2);
      cout << "+++++qIdxMem:" << qIdxMem << endl;
      if( fabs(qIdxMem) > floor( (pow(2,B) - 1) / 2) ) // saturation condition
	{
	  q = 0;
	}
      weight_Q += q;
      weight  -= q;
      cout << "q:" <<  q << endl;
    }
  cout << "=" << weight_Q << endl;
  return weight_Q;

}
