### 错误码
>错误码格式定义为6位数字，如：`2[XX][YYY]`。  
>其中XX表示模块编号，YYY是其内部提供的具体错误码。

#### 模块编号
```
00: 系统
01: 账号
```


#### 目前可能返回前端的错误码说明
```
--- 00: 系统 ---
1, '服务器内部错误，暂无法提供服务。'
200000, "未登录，无法访问"      // 无token
200001, "登录状态失效"         // token超时
200002, "未授权，无法访问"      // header不对


--- 01: 账号 ---
201001, '非超级管理员无法操作'
201002, '该用户已被禁止登录'
201003, '该用户不存在'
201004, '用户名或密码错误'
201005, '该账号已存在'
```