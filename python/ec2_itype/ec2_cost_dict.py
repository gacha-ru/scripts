#!/usr/bin/python
# coding:  utf8

ec2_cost_dict = {
    "t1.micro": 0.03,
    "m3.medium": 0.10,
    "m3.large": 0.20,
    "m3.xlarge": 0.41,
    "m3.2xlarge": 0.81,
    "m1.small": 0.06,
    "m1.medium": 0.12,
    "m1.large": 0.24,
    "m1.xlarge": 0.49,
    "c3.large": 0.13,
    "c3.xlarge": 0.26,
    "c3.2xlarge": 0.51,
    "c3.4xlarge": 1.02,
    "c3.8xlarge": 2.04,
    "c1.medium": 0.16,
    "c1.xlarge": 0.63,
    "cc2.8xlarge": 2.35,
    "g2.2xlarge": 0.90,
    "r3.large": 0.21,
    "r3.xlarge": 0.42,
    "r3.2xlarge": 0.84,
    "r3.4xlarge": 1.68,
    "r3.8xlarge": 3.36,
    "m2.xlarge": 0.29,
    "m2.2xlarge": 0.58,
    "m2.4xlarge": 1.15,
    "cr1.8xlarge": 4.11,
    "i2.xlarge": 1.00,
    "i2.2xlarge": 2.00,
    "i2.4xlarge": 4.00,
    "i2.8xlarge": 8.00,
    "hs1.8xlarge": 5.40,
    "hi1.4xlarge": 3.28,
    "t2.micro": 0.02,
    "t2.small": 0.04,
    "t2.medium": 0.080
}


ec2_oregon_cost_dict = {
    "t1.micro": 0.020,
    "t2.micro": 0.013,
    "t2.small": 0.026,
    "t2.medium": 0.052,
    "m3.medium": 0.070,
    "m3.large": 0.140,
    "m3.xlarge": 0.280,
    "m3.2xlarge": 0.560,
    "c3.large": 0.105,
    "c3.xlarge": 0.210,
    "c3.2xlarge": 0.420,
    "c3.4xlarge": 0.840,
    "c3.8xlarge": 1.680,
    "g2.2xlarge": 0.650,
    "r3.large": 0.175,
    "r3.xlarge": 0.350,
    "r3.2xlarge": 0.700,
    "r3.4xlarge": 1.400,
    "r3.8xlarge": 2.800,
    "i2.xlarge": 0.853,
    "i2.2xlarge": 1.705,
    "i2.4xlarge": 3.410,
    "i2.8xlarge": 6.820,
    "hs1.8xlarge": 4.600,
    "m1.small": 0.044,
    "m1.medium": 0.087,
    "m1.large": 0.175,
    "m1.xlarge": 0.350,
    "c1.medium": 0.130,
    "c1.xlarge": 0.520,
    "cc2.8xlarge": 2.000,
    "m2.xlarge": 0.245,
    "m2.2xlarge": 0.490,
    "m2.4xlarge": 0.980,
    "cr1.8xlarge": 3.500
}
