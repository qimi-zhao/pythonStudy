######################################
#
# 类名    ： clacmax
# 描述    ： 根据用户输入计算累加值
#
######################################
class clacmax:
    ######################################
    #
    # 主函数，流程控制
    # 入参 ： *numbers 不定个数int数据
    # 返回值： sum 返回值
    #
    ######################################
    def main(self, *numbers) -> int:
        input = []                                 # 定义 $输入数组
        for num in numbers:                        # 根据输入数量分次读入数据
            arr = self.getInput(num)               # 读取数据
            if arr == None:                        # 读取失败的情况下返回错误
                print("入力データ違うです！") 
            else:                                  # 读取成功的情况下加入到 $输入数组
                input.append(arr)
        
        sum = 0                                    # 定义返回值
        for val in input:                          # 根据 $输入数组 的成员数量进行累加
            sum += self.sumAll(val)                # 计算此次成员变量和
            print("現在の累積値は%dです." % (sum))    # 打印当前累加值

        return sum                                 # 返回计算结果
    
    ######################################
    #
    # 从控制台获取用户输入
    # 入参  ： num 本次要获取的数据数量
    # 返回值： arr 获取到的数据数组
    #
    ######################################
    def getInput(self, num) -> int:
        errCnt = 0                                                                                      # 定义最大输入错误次数
        while errCnt < 2:
            arr = (input("Int型データを%d個入力してください。','で区切られた！\n" % (num))).split(',')          # 获取输入值
            if len(arr) == num:
                return arr
            else:
                errCnt += 1
        return None
    
    ######################################
    #
    # 计算一次累加值
    # 入参 ： arr  输入数据
    #
    ######################################
    def sumAll(self, arr) -> int:
        min = int(arr[0])                        # 将数组第一个值设为当前最小值
        sum = 0                                  # 定义返回值
        for num in arr:
            num = int(num)                       # 将输入的str强制类型转换为int
            min = min if min < num else num      # 寻找数组内最小值
            sum += num                           # 计算所有数组成员的和
        return (sum - min)                       # 返回减去最小值的和

# 实例化对象
col = clacmax()
# 计算并打印
print(col.main(4, 2))
# 计算并打印
print(col.main(2, 2, 2, 2))
