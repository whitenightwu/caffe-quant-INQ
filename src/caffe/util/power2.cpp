#include "caffe/util/power2.hpp"
#include "caffe/common.hpp"
#include <math.h>
#include <iostream>

namespace caffe
{
  template <typename Dtype>
  double weightCluster( Dtype weight, int M)
  {
    double min=100;
    double ind=0;
    double flag=1.0;
    if(min>std::abs(weight))
    {
      min=std::abs(weight);
      flag=0.0;
    }
          
    for(int i=(M-7);i<=M;i++)
      {
        if(min>std::abs(weight-pow(2,i)))
          {
            min=std::abs(weight-pow(2,i));
            ind=i;
            flag=1.0;
          }
        if(min>std::abs(weight+pow(2,i)))
          {
            min=std::abs(weight+pow(2,i));
            ind=i;
            flag=-1.0;
          }
      }
      return flag*pow(2,ind);
  }
  
  template <typename Dtype>
  double weightCluster_zero( Dtype weight, int M)
  {
    double min=100;
    double ind=0;
    double flag=1.0;
    if(min>std::abs(weight))
    {
      min=std::abs(weight);
      flag=0.0;
    }
    //b=5     for(int i=(M-7);i<=M;i++)
    //b=4     for(int i=(M-3);i<=M;i++)
    for(int i=(M-7);i<=M;i++)
      {
        if(min>std::abs(weight-pow(2,i)))
          {
            min=std::abs(weight-pow(2,i));
            ind=i;
            flag=1.0;
          }
        if(min>std::abs(weight+pow(2,i)))
          {
            min=std::abs(weight+pow(2,i));
            ind=i;
            flag=-1.0;
          }
      }
      return flag*pow(2,ind);
  }

  template <typename Dtype>
  double shift_quantization(Dtype weight)
  {
    int N=2;
    int B=4;
    double weight_Q = 0;
    for(int n=0; n<N; n++)
      {
	float qSgn=1.0;
	if(weight<0)
	  qSgn=-1.0;
	double qLog = std::log(std::fabs(weight)) / std::log(2);
	double qIdx = std::floor(qLog);
	double bLog = qIdx + std::log(1.5)/std::log(2);
	if(qLog > bLog) // border condition
	  qIdx++;
	double q = qSgn * std::pow(2,qIdx);
	double qIdxMem = qSgn * (-(n+1)-qIdx+2);
	if( std::fabs(qIdxMem) > std::floor( (std::pow(2,B) - 1) / 2) ) // saturation condition
	  {
	    q = 0;
	  }
	weight_Q += q;
	weight  -= q;
    }
    return weight_Q;
  }


  template double weightCluster<float>(float weight,int M);
  template double weightCluster<double>(double weight,int M);
  template double weightCluster<unsigned int>(unsigned int weight,int M);
  template double weightCluster<int>(int weight,int M);
  template double weightCluster_zero<float>(float weight,int M);
  template double weightCluster_zero<double>(double weight,int M);
  template double weightCluster_zero<unsigned int>(unsigned int weight,int M);
  template double weightCluster_zero<int>(int weight,int M);

  template double shift_quantization<float>(float weight);
  template double shift_quantization<double>(double weight);
  template double shift_quantization<unsigned int>(unsigned int weight);
  template double shift_quantization<int>(int weight);

}
