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
    [CommandMeta("当天金融查票", 1)]
    public class 当天金融查票 : BaseMenuCommnad
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

            var ticket = "http://weixin.dtd365.com/index.php/home/ticket/myticketorder.html";

            var html = task.Client.Get(ticket);
            var doc = new HtmlAgilityPack.HtmlDocument();
            doc.LoadHtml(html);
            foreach (var comment in doc.DocumentNode.SelectNodes("//comment()").ToArray())
                comment.Remove();
            var text = doc.DocumentNode.SelectSingleNode("//ul[@class='order_ul']");
            if (text == null) return false;
            logger.Info(Regex.Replace(text.InnerText.Trim().Trim(), @"\s+", " "));
            return true;
        }
    }
}
