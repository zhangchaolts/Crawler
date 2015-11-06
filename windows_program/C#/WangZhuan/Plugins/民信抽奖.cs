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
    [CommandMeta("民信抽奖", 1)]
    public class 民信抽奖 : BaseMenuCommnad
    {


        protected override bool Run(AutoTaskContext task)
        {
            var uc = task.Client.Get("http://www.minxindai.com/?m=center");
            if (!uc.Contains("退出"))
            {
                var loginUrl = "http://www.minxindai.com/?m=user&c=login";
                var loginPost = "http://www.minxindai.com/?m=user&c=login&a=ulogin";

                var login = task.Client.Post(loginPost, new
                {
                    nickName = task.Mobile,
                    password = task.Pwd,
                    verifycode = "",
                    chkboxautologin = "false"
                }.ToDictionary(), CreateHeaders(loginUrl, isAjax: true));

                uc = task.Client.Get("http://www.minxindai.com/?m=center");
                if (!uc.Contains("退出"))
                {
                    logger.Error("登陆失败");
                    return false;
                }
                logger.Success("登陆成功");
            }

            var sign = task.Client.Post("http://www.minxindai.com/?m=event&c=jfturntab&a=islottery", new { }.ToDictionary(), CreateHeaders("http://www.minxindai.com/?m=event&c=jfturntab", isAjax: true));
            var json2 = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(sign);
            var name = (string)json2.name;
            logger.Info(name);
            return true;
        }
    }
}
