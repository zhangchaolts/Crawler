using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using WangZhuan.BaseFormLayout;
using Lj.Common;
using System.Net;
using System.Text.RegularExpressions;
using Newtonsoft.Json;
using System.Threading;
namespace WangZhuan
{
    [CommandMeta("当天金融签到", 1)]
    public class 当天金融签到 : BaseMenuCommnad
    {
        protected override bool Run(AutoTaskContext task)
        {

            var loginPage = "http://weixin.dtd365.com/index.php/home/account/login.html";

            var captcha = Recognize("http://wxticket.dtd365.com/index.php/home/index/getvcode.html");
            logger.Info("验证码：" + captcha);
            var data = new
            {
                username = task.Mobile,
                password = task.Pwd,
                captcha = captcha
            }.ToDictionary();
            var result = task.Client.Post("http://weixin.dtd365.com/index.php/home/index/getcode.html", data, CreateHeaders(loginPage, isAjax: true));
            var loginJson = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(result);
            if ((int)loginJson.status != 0)
            {
                logger.Error("登陆失败");
                return Run(task);
            }

            logger.Success("登陆成功");

            var statusHtml = task.Client.Get("http://weixin.dtd365.com/index.php/home/activity/showsign.html");
            if (statusHtml.Contains(@"id=""showsign_status"" value=""1"""))
            {
                var m = Regex.Match(statusHtml, @"<p>已签到<br><span>(\d+)<").Get(1);
                logger.Info("今日已签到，已签到" + m + "天");
                return false;
            }

            var x = task.Client.Post("http://weixin.dtd365.com/index.php/home/activity/activitysign.html", new { }.ToDictionary(), CreateHeaders("http://weixin.dtd365.com/index.php/home/activity/showsign.html", isAjax: true));
            var json = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(x);

            var statusHtml2 = task.Client.Get("http://weixin.dtd365.com/index.php/home/activity/showsign.html");
            if ((int)json.code == 1)
            {
                var hongbao = ((string)json.hongbao).To(0M);
                var m = Regex.Match(statusHtml2, @"<p>已签到<br><span>(\d+)<").Get(1);
                var hbt = hongbao > 0 ? ",获得红包:" + hongbao : "";
                logger.Success("签到成功，已签到" + m + "天" + hbt);
            }
            else
            {
                logger.Error("签到失败.");
            }

            return true;
        }
    }
}
