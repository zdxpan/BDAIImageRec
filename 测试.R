blanknum = read('/Users/zhoudaoxian/Desktop/1(1).csv',header = F,sep = ',')

blanknum <- read.table(pipe("pbpaste"), sep="\t", header=F)

name_t = c('user_id','click','search_id','query','winfoid','word_id','idea_id','term')
names(blanknum) = name_t

as.integer(blanknum[,'ship_order'])
class(blanknum[1,'ship_order'])
blanknum[1,'ship_order']



order_num = read.table(pipe("pbpaste"),sep = ",",header = F)
write.csv(order_num,file = "/Users/zhoudaoxian/Desktop/1.csv", row.names = F)


rm(blanknum,name_t,order_num)

order_num = read.delim("/Users/zhoudaoxian/Downloads/xac.csv",sep = ",",header = F)
names(order_num)=c('user_id','ztc_acct_name,idea_id','winfo_id','idea_name','show_word','new_trade_1_id',
  'new_trade_1_name','new_trade_2_id','new_trade_2_name','new_trade_3_id',
  'new_trade_3_name','charges','pcdv','clicks','sys_word_fun')
View(order_num[1:20,])


## '直通车系统问题导致客户投诉情况处理'
ztc_ = read.table(pipe("pbpaste"),sep = '\t',header = T)
ztc_7 = read.csv('/Users/zhoudaoxian/Desktop/ztc_1117.csv',header = F)
ztc_8 = read.csv('/Users/zhoudaoxian/Desktop/ztc_1108.csv',header = F)


c("user_id","plan_id","idea_id","click","charge","click_time")


print(ztc_[,1])

names(ztc)
names(ztc_uid) = "user_id"
ztc_uid$errflg = 1
library(dplyr)
# ztc = group_by(ztc)
ztc = rbind(ztc_7,ztc_8)
names(ztc) = c("user_id","plan_id","idea_id","click","charge","click_time")
ztc = left_join(ztc,ztc_,by = c('user_id','idea_id'))
ztc = ztc[!is.na(ztc$company),]
ztc$click_time = as.character(ztc$click_time)


write.csv(ztc,'/Users/zhoudaoxian/Desktop/ztc.csv',row.names = F)
split.Date(ztc$click_time[1],f = "%d %b %Y")
split(ztc$click_time[1],f = "%d %b %Y")



fc_r7 = read.csv('/Users/zhoudaoxian/Downloads/fc_reb_7.csv',header = F,stringsAsFactors = F)
fc_r8 = read.csv('/Users/zhoudaoxian/Downloads/fc_reb_8.csv',header = F,stringsAsFactors = F)
fc = rbind(fc_r7,fc_r8)
names(fc) = c("event_hour","event_minute","plan_id","idea_id","fcadclick_2_charge","fcadclick_2_bid")
fc = left_join(fc,ztc_,by = c('plan_id'))
fc = fc[!is.na(fc$user_id), ]

names(ztc_) = c('user_id','idea_id','saler','company','errtime')

library(dplyr)

ztc_ = read.csv('/Users/zhoudaoxian/Desktop/xxx.txt',header = T,stringsAsFactors = F,sep = '\t')
names(ztc_) = c('user_id','ztc_idea_id','idea_id','plan_id')

fc7 = read.csv('/Users/zhoudaoxian/Downloads/fc7.csv',header = F,stringsAsFactors = F)
fc7$V9 = 7
fc8 = read.csv('/Users/zhoudaoxian/Downloads/fc8.csv',header = F,stringsAsFactors = F)
fc8$V9 = 8
fc=rbind(fc7,fc8)
names(fc) = c('event_hour','event_minute','user_id','plan_id','idea_id','charge','click','show_time',"day")
# names(ztc_)[2] = 'plan_id'
fc = left_join(fc,ztc_,c("user_id","plan_id","idea_id"))
# n_fc = left_join(ztc_,fc,c("user_id","idea_id") )
# 1 ===============
fc= fc[!is.na(fc$ztc_idea_id),]
#  没有出现的结果是
n_fc= fc[is.na(fc$ztc_idea_id),]
fc_nofiltertime=fc%>%
  mutate(dh=paste(day,event_hour,sep = '_=_')) %>%
  group_by(user_id,ztc_idea_id,plan_id.x,dh) %>%
  summarise(
    charge=sum(charge),
    click=n()
  ) %>% 
  mutate(charge = charge/100)
## 查看临时数据
View(
  rbind(
  fc_nofiltertime[fc_nofiltertime$user_id==26234532,] %>% 
    filter(day==7) %>%
    filter(event_hour>=18),
  fc_nofiltertime[fc_nofiltertime$user_id==26234532,] %>% 
    filter(day==8) %>%
    filter(event_hour<=12)
  )
     )
## 讲过吕后的数据按照天，小时，planid,userid .ztc——idea_id 分组统计
fc_filtertime=rbind(fc1,fc2) %>%
  mutate(dh=paste(day,event_hour,sep = '_=_')) %>%
  group_by(user_id,ztc_idea_id,plan_id,dh) %>%
  summarise(
    charge=sum(charge),
    click=n()
  ) %>% 
  mutate(charge = charge/100)


# setdiff(unique(ztc_$idea_id), unique(fc$idea_id))
fc1 = rbind( fc %>%
  filter(day==7) %>%       # 433879 
  filter(event_hour>=18)   # 68508 
  ,
  fc %>%
  filter(day==8) %>%       #  353449
  filter(event_hour<12)    #  109733
)

fc2 = fc %>%              #  89029
    filter(day==7) %>%
    filter(event_hour>=12 & event_hour<14)

fcg1=fc1 %>%
  group_by(user_id,ztc_idea_id) %>%
  summarise(
    charge=sum(charge),
    click=n()
  ) %>%
  mutate(charge=charge/100)
fcg2=fc2 %>%
  group_by(user_id,ztc_idea_id) %>%
  summarise(
    charge=sum(charge),
    # plan_id=plan_id,
    click=n()
  ) %>%
  mutate(charge=charge/100)
fcg = full_join(fcg1,fcg2,by=c('user_id','ztc_idea_id')) %>%
  mutate(charge=charge.x+charge.y)
fcg[is.na(fcg$charge.x),'charge.x']=0
fcg[is.na(fcg$charge.y),'charge.y']=0
fcg$charge=fcg$charge.x+fcg$charge.y
# 2 warning  🐜 有错

# all 全部包括不匹配的和时间段之外的
not_mat_fcg = left_join(ztc_, fcg[,c(1,2,7)], by=c('user_id','ztc_idea_id') )
not_mat_fcg = not_mat_fcg[is.na(not_mat_fcg$charge),]
# 时间段之外的
outer_fcg = left_join(not_mat_fcg,fc_nofiltertime[,c(1,2,3,4)], by=c('user_id','ztc_idea_id') )
outer_fcg[is.na(outer_fcg$dh),'all'] = 2
outer_fcg = outer_fcg[,-5]

write.csv(fcg,'/Users/zhoudaoxian/Desktop/fcg.csv',row.names = F)
# 对应不上的那四个结果是：
write.csv(outer_fcg,'/Users/zhoudaoxian/Desktop/fcg时间之外.csv',row.names = F)

write.csv(fc_nofiltertime,'/Users/zhoudaoxian/Desktop/fc_nofiltertime.csv',row.names = F)
write.csv(fc_filtertime,'/Users/zhoudaoxian/Desktop/fc_filtertime.csv',row.names = F)

er.s = fc[fc$user_id==26010127 & fc$ztc_idea_id == 2101181,]
er.s = fcg[fcg$user_id==26010127 & fcg$ztc_idea_id == 2101181,]


王博文 = read.csv(pipe("pbpaste"),sep = '\t',header = F)
write.csv(王博文,"/Users/zhoudaoxian/Desktop/王博文.csv",row.names = F)
rm(王博文)

ztc_gold = read.csv("/Users/zhoudaoxian/Desktop/change.txt",header = T, sep = '\t')
write.csv(ztc_gold, "/Users/zhoudaoxian/Desktop/金银牌用户.csv" , row.names = F)
