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
    [CommandMeta("爱钱进抽奖", 1)]
    public class 爱钱进抽奖 : BaseMenuCommnad
    {


        protected override bool Run(AutoTaskContext task)
        {

            var home = task.Client.Get("http://www.iqianjin.com/userCenter/index");
            if (!home.Contains("用户中心"))
            {
                var loginUrl = "https://www.iqianjin.com/user/login";
                var loginPost = "https://www.iqianjin.com/user/logon";
                var code = Recognize("https://www.iqianjin.com/user/getCode");
                logger.Info("验证码识别结果：" + code);
                var login = task.Client.Post(loginPost, new
                {
                    name = task.Mobile,
                    password = task.Pwd,
                    code = code
                }.ToDictionary(), CreateHeaders(loginUrl, isAjax: true));

                var json = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(login);
                if ((int)json.code != 1)
                {
                    logger.Error("登陆失败");
                    return false;
                }
                logger.Success("登陆成功");
            }
            var actUrl = "http://www.iqianjin.com/activity/20151103.jsp";
            var act = task.Client.Get(actUrl);
            var times = task.Client.Get("http://www.iqianjin.com/activity/nov/myLotteryTimes?act=49&_=" + DateTime.Now.ToTimestamp(), actUrl);
            var timeJson = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(times);
            var time = (int)timeJson.bean.unUsedTimes;
            logger.Info("您有" + time + "次抽奖机会");
            if (time > 0)
            {
                var result = task.Client.Get("http://www.iqianjin.com/activity/nov/novLotteryAward?act=49&_=" + DateTime.Now.ToTimestamp(), actUrl);
                logger.Info(result);
                var json2 = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(result);
                if ((int)json2.code != 1)
                {
                    logger.Error((string)json2.message);
                    return false;
                }
                else
                {
                    logger.Info((string)json2.bean.name);
                }
            }
            return true;
        }
    }
}
