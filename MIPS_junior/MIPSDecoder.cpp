// decode the MIPS instructions; Input: a MIPS instruction;Process: Decode the instruction according to MIPS ISA
// Output: Operation,Source Operands,Destination Operand (total 4)
// Check the validness(是否存在，return false)
// sw=暫存器的東西放到記憶體,lw=記憶體的東西載到暫存器
//add&sub有4個(Instruction、Destination、Source1&2)；sw&lw有3個(Instruction、Destination、Source)
#include <iostream>
#include <string>
using namespace std;
int InsType(string Instructionstr);//判斷指令類型
bool CheckRegister(string tmpStr);//判斷Register輸入格式
string Instruction1[2] = {"add", "sub"};
string Instruction2[2] = {"lw", "sw"};//Data Transfer
string Register[32] = {
    "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
    "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
    "s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
    "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
};
int RegSize = 32;//有32個register
int InstructionSize1 = 2;//add,sub instruction
int InstructionSize2 = 2;//sw,lw instruction

int InsType(string Instructionstr)//判斷指令類型
{
     for (int x = 0; x < InstructionSize1;x++)//add,sub
     {
          if(Instructionstr==Instruction1[x]){return 1;}
     }
     for (int y = 0; y < InstructionSize2;y++)//lw,sw
     {
          if(Instructionstr==Instruction2[y]){return 2;}
     }
     cout << "Instruction Error.\n";
     return 0;
}

bool CheckRegister(string tmpStr)//檢查Register
{
     //Register名稱是否正確
     if (tmpStr=="$t0"||tmpStr =="$t1"||tmpStr=="$t2"||tmpStr=="$t3"||tmpStr=="$t4"||tmpStr=="$t5"||tmpStr =="$t6"||
          tmpStr=="$t7"||tmpStr =="$t8"||tmpStr=="$t9")
          {return 1;}
     else if (tmpStr=="$s0"||tmpStr=="$s1"||tmpStr=="$s2"||tmpStr=="$s3"||tmpStr=="$s4"||tmpStr=="$s5"||tmpStr=="$s6"||
          tmpStr=="$s7")
          {return 1;}
     else if (tmpStr=="$0"||tmpStr=="$1"||tmpStr=="$2"||tmpStr=="$3"||tmpStr=="$4"||tmpStr=="$5"||tmpStr=="$6"||tmpStr=="$7"||
          tmpStr=="$8"||tmpStr=="$9"||tmpStr=="$10"||tmpStr=="$11"||tmpStr=="$12"||tmpStr=="$13"||tmpStr=="$14"||tmpStr=="$15"||
          tmpStr=="$16"||tmpStr=="$17"||tmpStr=="$18"||tmpStr=="$19"||tmpStr=="$20"||tmpStr=="$21"||tmpStr=="$22"||tmpStr=="$23"||
          tmpStr=="$24"||tmpStr=="$25"||tmpStr=="$26"||tmpStr=="$27"||tmpStr=="$28"||tmpStr=="$29"||tmpStr=="$30"||tmpStr=="$31")
          {return 1;}
     //輸入format
     else if (tmpStr[0] == '$')//條件:數值
     {
        string NumStr = "";//初始
        for (int i = 1; i < tmpStr.length(); i++)//從1開始，0~31
        {
          NumStr = NumStr+tmpStr[i];
        }
        //條件:32bit,4=1
        if ((NumStr[0] <='9') && (NumStr[0] >= '1'))//條件1~9
        {
          for (int i = 1; i < NumStr.length(); i++)//for 32bit,4 bytes=1word->8
          {
               if ((NumStr[i] >= '9') || (NumStr[i] < '0'))//不該超過8
               {
                    cout << "Register format error." << endl;
                    return 0;
               }
               else{return 1;}
          }
          //只有0~31能用
          if ((atoi(NumStr.c_str()) < 1) || (atoi(NumStr.c_str()) > 32))//字串轉整數,C語言轉換,4=1
          {
               cout << "Register format error." << endl;//負數及大於31都不對
               return 0;
          }
          else{return 1;}
        }
        else
        {
          cout << "Register format error." << endl;
          return 0;
        }
     }
    //lw、sw會用到的，32bit->4bytes=1word,8 times
    else if ((tmpStr[0] >= '1') && (tmpStr[0] < '9')) // ex.32($t0)
    {
        string NumStr = "";
        for (int i=0; (tmpStr[i] >= '0') && (tmpStr[i] < '9'); i++)//在()前的0~9
        {
          NumStr=NumStr+tmpStr[i];//0~9合輸入
        }
        //read到"("
        int j = 0;
        if (tmpStr[j] == '('){return 1;}
        else
        {
          cout << "Registers format error." << endl;
          return 0;
        }
    }
    else
    {
        cout << "Registers format error." << endl;
        return 0;
    }
}
int main()
{
    string s;
    //輸入MIPS指令
    cout << "Please Enter MIPS instruction (ex. add $t0 $t1 $t2)\n";
    getline(cin, s);//把string輸進去

    //判斷command & register
    string Instructionstr="",str1="",str2="",str3="";//ex. add $t0 $t1 $t2
    int position = 0;//初始讀取位置
    //以下忽略空白格
     //Instruction
     for(;s[position]!=' ';position++){Instructionstr=Instructionstr+s[position];}
     position++;
     //Destination
     for(;s[position]!=' ';position++){str1=str1+s[position];}
     position++;
     //Source1 & Source2
     for (;(s[position] != ' ') && (position < s.length()); position++){str2=str2+s[position];}

     int InsNum = InsType(Instructionstr);//判斷指令類型
     if (InsNum == 1) // str3會存在的指令類型(add,sub)
     {
          position++;
          for (; (s[position] != ' ') && (position < s.length()); position++){str3=str3+s[position];}
     }
     //判斷指令是否正確，非1則2
     if (InsNum == 0){return 0;}
     //判斷register輸入格式
     if (CheckRegister(str1) == 0||CheckRegister(str2)==0){return 0;}
     if (InsNum == 1)//add,sub
     {
          if (CheckRegister(str3)==0)
          return 0;
     }
     //結果
     if ((Instructionstr == "add") || (Instructionstr == "sub")) // add, sub
     {
         cout<<"Instruction: " << Instructionstr << endl;
         cout<<"Source operands: " << str2 << ", " << str3 << endl;
         cout<<"Destination operand: " << str1 << endl;
     }
     else if (Instructionstr == "lw")
     {
         cout<<"Instruction: " << Instructionstr << endl;
         cout<<"Source operands(included address): " << str2 << endl;
         cout<<"Destination operand: " << str1 << endl;
         // cout<<"Address: "<<endl;
     }
     else if (Instructionstr == "sw")
     {
         cout<<"instruction: " << Instructionstr << endl;
         cout<<"Source operand(included address): " << str2 << endl;
         cout<<"Destination operand: " << str1 << endl;
         //cout << "Address: " << endl;
     }
     else{ cout<<"Error.\n";}
     return 0;
}