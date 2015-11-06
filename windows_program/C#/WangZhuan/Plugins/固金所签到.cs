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
    [CommandMeta("固金所签到", 1)]
    public class 固金所签到2 : BaseMenuCommnad
    {
        protected override bool Run(AutoTaskContext task)
        {
            var code = Recognize(() => "https://www.gujinsuo.com.cn/auth/random", 6);
            logger.Info("验证码识别结果");

            var result = task.Client.Post("https://www.gujinsuo.com.cn/login", new
            {
                username = task.Mobile,
                password = task.Pwd,
                randcode = code
            }.ToDictionary(), CreateHeaders("https://www.gujinsuo.com.cn/login.html",isAjax:true));
            logger.Trace(result);
            if (!result.Contains("true")) {
                logger.Error("登陆失败");
                return false;
            }
            logger.Success("登陆成功");

            var 签到 = task.Client.Get("https://www.gujinsuo.com.cn/spread/sign?_=" + new DateTime().ToTimestamp());
            var j = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(签到);
            if ((bool)j.success)
            {
                logger.Success((string)j.message);
            }
            else
            {
                logger.Error((string)j.message);
            }

            return false;
        }
    }
}
