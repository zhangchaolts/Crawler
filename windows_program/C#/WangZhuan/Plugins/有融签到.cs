using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using WangZhuan.BaseFormLayout;
using System.Windows.Forms;
using Lj.Common;
using System.Text.RegularExpressions;
using System.Net;

namespace WangZhuan.WuKong
{
    [CommandMeta("有融签到",0)]
    public class LoginMenuCommand : IMenuCommand
    {
        protected AutoTaskGridLogger logger;

        public bool Execute(AutoTaskContext task)
        {
            logger = new AutoTaskGridLogger(task);
            var client = task.Client;
            var account = task.Account;
            client.Encoding = Encoding.UTF8;

            //获取Form Token
            var resiterHtml = client.DownloadString("http://www.yourong.cn/security/login");
            var formTokenMatch = Regex.Match(resiterHtml, @"name=""xToken""\s+value=""(.*?)""");
            var formToken = formTokenMatch.Get(1);
            logger.Trace(account.Name + "表单Token:" + formToken);
            if (string.IsNullOrWhiteSpace(formToken))
            {
                logger.Info("获取Token失败,稍候重试!");
                return false;
            }

            //登陆
            var postRegisterUrl = "http://www.yourong.cn/security/logined";
            var headers = new WebHeaderCollection {
                                { "Referer","http://www.yourong.cn/security/login"},
                                { "Host","www.yourong.cn"},
                                { "Accept","*/*"},
                                { "X-Requested-With","XMLHttpRequest"},
                                { "Content-Type","application/x-www-form-urlencoded; charset=UTF-8"},
                                { "User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36" }
                        };

            var tel = account.Attributes.Get("[手机]").To("");
            var password = account.Attributes.Get("[密码]").To("");
            if (string.IsNullOrEmpty(tel) || !Regex.IsMatch(tel, @"\d{11}"))
            {
                logger.Error(account.Name + "手机号码不正确!");
                return false;
            }

            if (string.IsNullOrEmpty(password))
            {
                logger.Error(account.Name + "密码不能为空!");
                return false;
            }




            //登陆信息
            var loginData = new
            {
                xToken = formToken,
                username = tel,
                password = password,
                pngCode = "",
                loginSource = "0"
            }.ToDictionary();

            var loginResponse = client.Post(postRegisterUrl, loginData, headers);
            if (loginResponse.Contains("\"success\":true"))
            {
                logger.Info(account.Name + "登陆成功.");
            }
            else
            {
                logger.Error(account.Name + "登陆失败.");
                return false;
            }



            //签到
            var checkUrl = "http://www.yourong.cn/member/check/?_=" + (new DateTime()).ToTimestamp();
            var checkHeaders = new WebHeaderCollection {
                                { "Referer","http://www.yourong.cn/member/home"},
                                { "Host","www.yourong.cn"},
                                { "Accept","application/json, text/javascript, */*; q=0.01"},
                                { "X-Requested-With","XMLHttpRequest"},
                                { "User-Agent","Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36" }
                        };

            var checkResponse = client.Get(checkUrl, headers);
            try
            {
                var json = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(checkResponse);
                if ((bool)json.success)
                {
                    var value = (int)json.result.gainPopularity;
                    var popularityResponse = client.Get("http://www.yourong.cn/coupon/reputation");
                    var currentP = Regex.Match(popularityResponse, @"<span\s+id=""j-popularity-value"">(.*?)</span>").Get(1);
                    logger.Success(account.Name + "签到成功,恭喜您获得 " + value + " 点人气值,总人气值:" + currentP);
                }
                else
                {
                    var popularityResponse = client.Get("http://www.yourong.cn/coupon/reputation");
                    var currentP = Regex.Match(popularityResponse, @"<span\s+id=""j-popularity-value"">(.*?)</span>").Get(1);

                    logger.Error(account.Name + "签到失败，您已经签到过了,您的总人气值:" + currentP);
                }



                //var response = client.Get("http://www.yourong.cn/activity/yiRoad/index", checkHeaders);
                //var xToeknItem = Regex.Match(response, @"name=""xToken""\s+value=""(.*?)""");
                //var yiRoadToken = xToeknItem.Get(1);
                //logger.Trace(account.Name + "分享Token:" + yiRoadToken);

                //var post = client.Post("http://www.yourong.cn/activity/yiRoad/share", new { xToken = yiRoadToken }.ToDictionary(), checkHeaders);
                //var json2 = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(post);
                //var name = (string)json2.rewardName;


                //var popularityResponse2 = client.Get("http://www.yourong.cn/coupon/reputation");
                //var currentP2 = Regex.Match(popularityResponse2, @"<span\s+id=""j-popularity-value"">(.*?)</span>").Get(1);
                //logger.Success("分享获取" + name + ",总人气值:" + currentP2);

                
            }
            catch (Exception ex)
            {
                logger.Error(account.Name + "签到错误" + ex.Message);
                return false;
            }
            return true;
        }
    }
}
