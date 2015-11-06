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
    [CommandMeta("加薪猫抢标", 1)]
    public class 加薪猫抢标 : BaseMenuCommnad
    {

        static int tq = 5;
        static bool isSet = false;
        static object oLock = new object();
        string proId = string.Empty;
        
        protected override bool Run(AutoTaskContext task)
        {

            lock (oLock)
            {
                if (!isSet) {
                    logger.Info("设置提前若干秒来抢标，请根据自己的网络情况来决定，建议2秒");
                    var t = new MessageInputPanel();
                    tq = t.GetMessage("提前抢标时间（单位秒）：").To(0);
                    if (tq < 0) {
                        tq = 0;
                    }
                    logger.Info("提前" + tq + "秒发起抢标!");
                    isSet = true;
                }
            }

            var loginUrl = "http://m.jiaxinmore.com/#login";
            var loginPost = "http://m.jiaxinmore.com/apps/api/user/login";

            var loginText = task.Client.Post(loginPost, new
            {
                userId = task.Mobile,
                loginPwd = task.Pwd,
                captcha = ""
            }.ToDictionary(), CreateHeaders(loginUrl, isAjax: true));
            var loginJson = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(loginText);
            if (!loginText.Contains("成功"))
            {
                var msg = (string)loginJson.msg;
                logger.Error(msg);
                return false;
            }

            logger.Success("登陆成功");
            DateTime? saleStartTime = DateTime.Today.AddHours(10);

            lock (oLock)
            {
                if (string.IsNullOrEmpty(proId))
                {
                    //logger.Info("标的检索...");
                    
                    //for (var i = 20; i < 50; i++)
                    //{
                    //    var id = "GD15AG17000100" + i.ToString("00");
                    //    var u = "http://m.jiaxinmore.com/apps/api/product/detail?productNo=" + id;
                    //    var rText = task.Client.Get(u, CreateHeaders("http://m.jiaxinmore.com/", isAjax: true));
                    //    if (!rText.Contains("专为新手体验设计")) break;
                    //    var rJson = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(rText);
                    //    var pid = rJson.data.productNo;
                    //    saleStartTime = DateTime.Parse((string)rJson.data.saleStartTime);
                    //    if (saleStartTime.Value.Date == DateTime.Today)
                    //    {
                    //        logger.Info("今日标的ID：" + pid);
                    //        proId = pid;
                    //        break;
                    //    }
                    //}

                    //未发现标的ID，请输入
                    if (string.IsNullOrEmpty(proId))
                    {
                        var mbox = new MessageInputPanel();
                        proId = mbox.GetMessage("请输入标的PID：");
                    }

                    if (string.IsNullOrEmpty(proId))
                    {
                        logger.Error("未输入产品ID，投标任务停止");
                        return false;
                    }

                    logger.Info("投标目标ID：" + proId + ",开标时间：" + saleStartTime);
                }
            }

            if (DateTime.Now < saleStartTime)
            {
                logger.Info("等待开标中...");
            }

            var startTime = saleStartTime.Value.AddSeconds(-tq);
            while (true)
            {
                if (DateTime.Now > startTime) break;
                Thread.Sleep(20);
            }

            var isCreated = false;
            var orderNo = string.Empty;
            var reTry = 50;
            while (reTry > 0)
            {
                logger.Info("打开投标页面..");
                var jsonText = task.Client.Post("http://m.jiaxinmore.com/apps/api/order/toInvestConfirm", new { productNo = proId }.ToDictionary(), CreateHeaders("http://m.jiaxinmore.com/#list", isAjax: true));
                var json = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(jsonText);
                var ret = (int)json.ret;
                if (ret != 0)
                {
                    logger.Error("投标页面打开失败.");
                    reTry--;
                    Thread.Sleep(50);
                    continue;
                }

                var token = (string)json.data.token;
                logger.Info("订单创建中...");
                var confirmUrl = "http://m.jiaxinmore.com/apps/api/order/toInvestConfirm";
                var createUrl = "http://m.jiaxinmore.com/apps/api/order/createOrder";
                var createJosnText = task.Client.Post(createUrl, new
                {
                    productNo = proId,
                    investAmount = 1000,
                    token = token
                }.ToDictionary(), CreateHeaders(confirmUrl, isAjax: true));


                var createJson = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(createJosnText);
                var createRet = (int)createJson.ret;
                if (createRet != 0)
                {
                    var msg = (string)createJson.msg;
                    logger.Error("订单创建失败," + msg);
                    if (msg == "无可投金额")
                    {
                        return false;
                    }
                    Thread.Sleep(50);
                    reTry--;
                }
                else
                {
                    logger.Success("订单创建完成.");
                    isCreated = true;
                    orderNo = (string)createJson.data.orderNo;
                    break;
                }
            }

            if (isCreated)
            {
                logger.Info("开始支付订单：" + orderNo);
                var code = task.Wzc.PrivateSmsProvider.GetVcode(task, task.Mobile, 100000);
                logger.Info("支付手机验证码：" + code.Result);
                var payUrl = "http://m.jiaxinmore.com/apps/api/order/payOrder";
                var payData = new
                {
                    msgCode = code.Result,
                    transactPwd = task.TranPwd,
                    orderNo = orderNo
                }.ToDictionary();

                var payResult = task.Client.Post(payUrl, payData, CreateHeaders("http://m.jiaxinmore.com/", isAjax: true));
                if (payResult.Contains("成功"))
                {
                    logger.Success("订单支付完成.");
                }
                else
                {
                    logger.Error("订单支付失败：" + payResult);
                }
            }
            return true;
        }
    }
}
