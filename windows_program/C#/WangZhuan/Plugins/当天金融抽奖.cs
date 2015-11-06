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
    [CommandMeta("当天金融抽奖", 1)]
    public class 当天金融抽奖 : BaseMenuCommnad
    {


        protected override bool Run(AutoTaskContext task)
        {
            var loginPage = "http://weixin.dtd365.com/index.php/home/account/login.html";
            var captcha = Recognize("http://wxticket.dtd365.com/index.php/home/index/getvcode.html");
            logger.Info("验证码：" + captcha);
            try
            {

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
            }
            catch (Exception)
            {
                return Run(task);
            }



            while (true)
            {
                try
                {
                    logger.Info("正在执行抽奖...");
                    var signUrl = "http://weixin.dtd365.com/index.php/home/activity/getrotate.html";
                    var jsonText = task.Client.Post(signUrl, new { data = 1 }.ToDictionary(), CreateHeaders(loginPage, isAjax: true));
                    dynamic json = null;
                    try
                    {
                        json = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(jsonText);
                    }
                    catch (Exception)
                    {
                        return Run(task);
                    }
                    var code = (string)json.code;
                    var msg = (string)json.message;
                    if (code == "500")
                    {
                        logger.Error(msg);
                        break;
                    }
                    else if (code == "200")
                    {
                        var lotteryAwardsId = (int)json.result.lotteryAwardsId;
                        var awardsName = (string)json.result.awardsName;
                        var awardsMoney = (decimal)json.result.awardsMoney;
                        if (!new[] { 5, 7, 12 }.Contains(lotteryAwardsId))
                        {
                            logger.Fatal(awardsName + " : " + awardsMoney);
                        }
                        else
                        {
                            if (awardsMoney > 95)
                            {
                                logger.Fatal(awardsName + " : " + awardsMoney);
                            }
                            else
                            {
                                logger.Info(awardsName + " : " + awardsMoney);
                            }
                        }
                    }
                    else
                    {
                        logger.Info(jsonText);
                    }
                }
                catch (Exception ex)
                {
                    logger.Error("抽奖操作错误：" + ex.Message);
                }
            }

            return true;
        }
    }
}
