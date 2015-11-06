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
    [CommandMeta("民信签到", 1)]
    public class 民信签到 : BaseMenuCommnad
    {


        protected override bool Run(AutoTaskContext task)
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

            var uc = task.Client.Get("http://www.minxindai.com/?m=center");
            if (!uc.Contains("退出"))
            {
                logger.Error("登陆失败");
                return false;
            }

            logger.Success("登陆成功");
            



            /*
            var juanUrl = "http://www.minxindai.com/?m=center&c=coupon&a=index";
            var juan = task.Client.Get(juanUrl);
            var doc2 = new HtmlAgilityPack.HtmlDocument();
            doc2.LoadHtml(juan);
            var juanNodes = doc2.DocumentNode.SelectNodes(".//li[@class='coupon-content xjy-ky']");
            if (juanNodes != null)
            {
                logger.Info("---------------------------");
                foreach (var n in juanNodes)
                {
                    var cls = n.SelectSingleNode("./div[1]").Attributes["class"].Value;
                    var amount = Regex.Match(cls, @".*?(\d+)").Get(1, 0);
                    var isRed = false;
                    if (amount < 5)
                    {
                        logger.Info("加息卷额度" + amount + "%");
                    }
                    else
                    {
                        logger.Info("红包金额:" + amount + "元");
                        isRed = true;
                    }
                    var name = Regex.Replace(n.SelectSingleNode(".//div[@class='xjq_1']").InnerText.Trim().Replace("\n", "|"),@"\s","");
                    name.Split('|').ForEach(x => logger.Info(x));
                    var mask = Regex.Replace(n.SelectSingleNode(".//div[@class='mask']").InnerText.Trim().Replace("\n", "|"), @"\s", "");
                    mask.Split('|').ForEach(x => logger.Info(x));
                    logger.Info("---------------------------");
                }
            }
            */


            var sign = task.Client.Post("http://www.minxindai.com/?c=sign", new { }.ToDictionary(), CreateHeaders("http://www.minxindai.com/?m=center", isAjax: true));
            var json2 = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(sign);
            var msg = (string)json2.signsate;
            msg = msg.Replace("<em>", "").Replace("</em>", "").Replace("<i>", "").Replace("</i>", "");
            logger.Info(msg);


            var share = task.Account.Read("民信分享");
            if (!string.IsNullOrWhiteSpace(share))
            {
                var rt = task.Client.Get(share);
                logger.Info("民信分享完成.");
            }

            var cj = task.Client.Get("http://www.minxindai.com/?m=event&c=jfturntab");
            var scores = Regex.Match(cj, @"scores"">(\d+)<").Get(1);
            uc = task.Client.Get("http://www.minxindai.com/?m=center");
            var doc = new HtmlAgilityPack.HtmlDocument();
            doc.LoadHtml(uc);
            var node = doc.DocumentNode.SelectSingleNode("//div[@class='edu-wp']");
            var li1 = node.SelectSingleNode(".//li[1]/span[@class='ff-r']").InnerText;
            var li2 = node.SelectSingleNode(".//li[2]/span[@class='ff-r']").InnerText;
            logger.Info("账户总资产：" + li1 + "，可用余额：" + li2 + ",可用积分：" + scores);


            return true;
        }
    }
}
