using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using WangZhuan.BaseFormLayout;
using Lj.Common;
using System.Net;
using System.Text.RegularExpressions;
using Newtonsoft.Json;
namespace WangZhuan
{
    [CommandMeta("金融工场签到", 1)]
    public class 金融工场签到 : BaseMenuCommnad
    {


        protected override bool Run(AutoTaskContext task)
        {

            //检验是否需要验证码
            var safeVerifyUrl = "https://passport.9888.cn/passport/saftverify/verify?verifyusername=" + task.Mobile;


            var loginUrl = "https://passport.9888.cn/passport/login";

            var loginHtml = _task.Client.Get(loginUrl);

            var loginName = string.IsNullOrEmpty(task.Uid) ? task.Mobile : task.Uid;

            if (!loginHtml.Contains("http://www.9888.cn?islogin=true&pc=1"))
            {
                var form = XFormHelper.Serialize(loginHtml, "myLoginForm", new Dictionary<string, object> { 
                    { "username" , loginName },
                    { "password" , task.Pwd },
                    { "addinput","密码" }
                });


                var uc = _task.Client.Post(loginUrl, form, CreateHeaders(loginUrl));


                if (!uc.Contains("http://www.9888.cn?islogin=true&pc=1"))
                {
                    logger.Error("登陆失败");
                    return false;
                }
                logger.Success("登陆成功");
            }

            
            var home = task.Client.Get("http://www.9888.cn/account/home.shtml");
            var gd = Regex.Match(home, @"class=""bl"">(\d+)<").Get(1, 0);
            logger.Info("工豆数量" + gd);
            

            var signResult = task.Client.Get("http://www.9888.cn/account/signMethod.do?_"+new DateTime().ToTimestamp());

            var json2 = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(signResult);
            var flag = (string)json2.flag;
            var total = (decimal)json2.G_AVAILABLE_BALANCE;
            
            if (flag == "success")
            {

                var returnAmount = (int)json2.returnAmount;
                logger.Success("签到完成,获得工豆:" + returnAmount + ",工豆总计：" + total);
                var win = (string)json2.win == "true";
                if (win)
                {
                    var redPageAccount = (decimal)json2.redPageAccount;
                    logger.Info("签到获得一个红包，金额:" + redPageAccount);
                }
            }
            else if(flag == "already")
            {

                logger.Info("您已签到过,工豆总计:" + total);
            }


            var hb = task.Client.Get("http://www.9888.cn/redPackage/bigPackageDatalist.do?rows=50&page=1");
            var json = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(hb);
            var result = json.pageData.result;
            foreach (var o in result)
            {
                var validTime = DateTime.Parse((string)o.applyValidTime);
                if (validTime > DateTime.Now)
                {
                    logger.Fatal("红包记录：" + ((int)o.id).ToString() + "，过期时间：" + (string)o.applyValidTime);
                }
            }
            return true;
        }
    }
}
