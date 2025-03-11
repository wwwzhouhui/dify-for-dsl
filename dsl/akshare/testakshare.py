from datetime import datetime, timedelta
import pandas as pd
import json
# from logger import get_logger
# # 获取日志器


# logger = get_logger()

params = {
            'ma_periods': {'short': 5, 'medium': 20, 'long': 60},
            'rsi_period': 14,
            'bollinger_period': 20,
            'bollinger_std': 2,
            'volume_ma_period': 20,
            'atr_period': 14
        }
def get_recommendation(score):
        """根据得分给出建议"""
        print(f"根据评分 {score} 生成投资建议")
        if score >= 80:
            return '强烈推荐买入'
        elif score >= 60:
            return '建议买入'
        elif score >= 40:
            return '观望'
        elif score >= 20:
            return '建议卖出'
        else:
            return '强烈建议卖出'
def calculate_score(df):
        """计算评分"""
        try:
            score = 0
            latest = df.iloc[-1]
            
            # 趋势得分 (30分)
            if latest['MA5'] > latest['MA20']:
                score += 15
            if latest['MA20'] > latest['MA60']:
                score += 15
                
            # RSI得分 (20分)
            if 30 <= latest['RSI'] <= 70:
                score += 20
            elif latest['RSI'] < 30:  # 超卖
                score += 15
                
            # MACD得分 (20分)
            if latest['MACD'] > latest['Signal']:
                score += 20
                
            # 成交量得分 (30分)
            if latest['Volume_Ratio'] > 1.5:
                score += 30
            elif latest['Volume_Ratio'] > 1:
                score += 15
                
            return score
            
        except Exception as e:
            print(f"计算评分时出错: {str(e)}")
            raise
def calculate_ema(series, period):
        """计算指数移动平均线"""
        return series.ewm(span=period, adjust=False).mean()
def calculate_rsi(series, period):
        """计算RSI指标"""
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

def calculate_macd(series):
        """计算MACD指标"""
        exp1 = series.ewm(span=12, adjust=False).mean()
        exp2 = series.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        hist = macd - signal
        return macd, signal, hist
def calculate_bollinger_bands(series, period, std_dev):
        """计算布林带"""
        middle = series.rolling(window=period).mean()
        std = series.rolling(window=period).std()
        upper = middle + (std * std_dev)
        lower = middle - (std * std_dev)
        return upper, middle, lower
        
def calculate_atr(df, period):
        """计算ATR指标"""
        high = df['high']
        low = df['low']
        close = df['close'].shift(1)
        
        tr1 = high - low
        tr2 = abs(high - close)
        tr3 = abs(low - close)
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean()
def calculate_indicators(df):
        """计算技术指标"""
        try:
            # 计算移动平均线
            df['MA5'] = calculate_ema(df['close'], params['ma_periods']['short'])
            df['MA20'] = calculate_ema(df['close'], params['ma_periods']['medium'])
            df['MA60'] = calculate_ema(df['close'], params['ma_periods']['long'])
            
            # 计算RSI
            df['RSI'] = calculate_rsi(df['close'], params['rsi_period'])
            
            # 计算MACD
            df['MACD'], df['Signal'], df['MACD_hist'] = calculate_macd(df['close'])
            
            # 计算布林带
            df['BB_upper'], df['BB_middle'], df['BB_lower'] = calculate_bollinger_bands(
                df['close'],
                params['bollinger_period'],
                params['bollinger_std']
            )
            
            # 成交量分析
            df['Volume_MA'] = df['volume'].rolling(window=params['volume_ma_period']).mean()
            df['Volume_Ratio'] = df['volume'] / df['Volume_MA']
            
            # 计算ATR和波动率
            df['ATR'] = calculate_atr(df, params['atr_period'])
            df['Volatility'] = df['ATR'] / df['close'] * 100
            
            # 动量指标
            df['ROC'] = df['close'].pct_change(periods=10) * 100
            
            return df
            
        except Exception as e:
            print(f"计算技术指标时出错: {str(e)}")
            raise
def _truncate_json_for_logging(json_obj, max_length=500):
        """截断JSON对象用于日志记录，避免日志过大
        
        Args:
            json_obj: 要截断的JSON对象
            max_length: 最大字符长度，默认500
            
        Returns:
            str: 截断后的JSON字符串
        """
        json_str = json.dumps(json_obj, ensure_ascii=False)
        if len(json_str) <= max_length:
            return json_str
        return json_str[:max_length] + f"... [截断，总长度: {len(json_str)}字符]"
def get_stock_data(self, stock_code, market_type='A', start_date=None, end_date=None):
        """获取股票或基金数据"""
        import akshare as ak
        
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y%m%d')
            
        try:
            # 验证股票代码格式
            if market_type == 'A':
                # 上海证券交易所股票代码以6开头
                # 深圳证券交易所股票代码以0或3开头
                # 科创板股票代码以688开头
                # 北京证券交易所股票代码以8开头
                valid_prefixes = ['0', '3', '6', '688', '8']
                valid_format = False
                
                for prefix in valid_prefixes:
                    if stock_code.startswith(prefix):
                        valid_format = True
                        break
                
                if not valid_format:
                    error_msg = f"无效的A股股票代码格式: {stock_code}。A股代码应以0、3、6、688或8开头"
                    # logger.error(f"[股票代码格式错误] {error_msg}")
                    raise ValueError(error_msg)

                df = ak.stock_zh_a_hist(
                    symbol=stock_code,
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq"
                )
            elif market_type == 'HK':
                df = ak.stock_hk_daily(
                    symbol=stock_code,
                    adjust="qfq"
                )
            elif market_type == 'US':
                df = ak.stock_us_hist(
                    symbol=stock_code,
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq"
                )
            elif market_type == 'ETF':
                df = ak.fund_etf_hist_em(
                    symbol=stock_code,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq"
                )
            elif market_type == 'LOF':
                df = ak.fund_lof_hist_em(
                    symbol=stock_code,
                    period="daily",
                    start_date=start_date,
                    end_date=end_date,
                    adjust="qfq"
                )
            else:
                raise ValueError(f"不支持的市场类型: {market_type}")
            
            # 重命名列名以匹配分析需求
            df = df.rename(columns={
                "日期": "date",
                "开盘": "open",
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume"
            })
            
            # 确保日期格式正确
            df['date'] = pd.to_datetime(df['date'])
            
            # 数据类型转换
            numeric_columns = ['open', 'close', 'high', 'low', 'volume']
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
            
            # 删除空值
            df = df.dropna()
            
            return df.sort_values('date')
            
        # except ValueError as ve:
        #     # 捕获格式验证错误
        #     logger.error(f"[股票代码格式错误] {str(ve)}")
        #     raise Exception(f"股票代码格式错误: {str(ve)}")
        except Exception as e:
            raise Exception(f"获取数据失败: {str(e)}")
        
stock_code='600271'
market_type='A'
stock_zh_a_hist_df=get_stock_data("",stock_code,market_type)
print(stock_zh_a_hist_df)
recent_data = stock_zh_a_hist_df.tail(14).to_dict('records')
print(recent_data)




# 计算技术指标
print(f"计算 {stock_code} 技术指标")
stock_zh_a_hist_df = calculate_indicators(stock_zh_a_hist_df)
# 评分系统
print(f"计算 {stock_code} 评分")
score = calculate_score(stock_zh_a_hist_df)
print(f"{stock_code} 评分结果: {score}")
            
# 获取最新数据
latest = stock_zh_a_hist_df.iloc[-1]
prev = stock_zh_a_hist_df.iloc[-2]
            
            # 生成报告
report = {
                'stock_code': stock_code,
                'market_type': market_type,  # 添加市场类型
                'analysis_date': datetime.now().strftime('%Y-%m-%d'),
                'score': score,
                'price': latest['close'],
                'price_change': (latest['close'] - prev['close']) / prev['close'] * 100,
                'ma_trend': 'UP' if latest['MA5'] > latest['MA20'] else 'DOWN',
                'rsi': latest['RSI'] if not pd.isna(latest['RSI']) else None,
                'macd_signal': 'BUY' if latest['MACD'] > latest['Signal'] else 'SELL',
                'volume_status': 'HIGH' if latest['Volume_Ratio'] > 1.5 else 'NORMAL',
                'recommendation': get_recommendation(score)
            }
print(f"生成 {stock_code} 基础报告: {_truncate_json_for_logging(report, 500)}...")

technical_summary = {
                'trend': 'upward' if stock_zh_a_hist_df.iloc[-1]['MA5'] > stock_zh_a_hist_df.iloc[-1]['MA20'] else 'downward',
                'volatility': f"{stock_zh_a_hist_df.iloc[-1]['Volatility']:.2f}%",
                'volume_trend': 'increasing' if stock_zh_a_hist_df.iloc[-1]['Volume_Ratio'] > 1 else 'decreasing',
                'rsi_level': stock_zh_a_hist_df.iloc[-1]['RSI']
}
print(technical_summary)

prompt = f"""
 分析A股 {stock_code}：
 技术指标概要：
{technical_summary}
近14日交易数据：
{recent_data}
请提供：
1. 趋势分析（包含支撑位和压力位）
2. 成交量分析及其含义
3. 风险评估（包含波动率分析）
4. 短期和中期目标价位
5. 关键技术位分析
6. 具体交易建议（包含止损位）
请基于技术指标和A股市场特点进行分析，给出具体数据支持。
 """

print(f"生成的AI分析提示词: {prompt}...")
#print(f"生成的AI分析提示词: {_truncate_json_for_logging(prompt, 1000)}...")
# import akshare as ak

# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20231022', adjust="")
# print(stock_zh_a_hist_df)