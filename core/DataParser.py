from bs4 import BeautifulSoup
import html
import json

# 知乎用户信息字段
# 用户头像
USER_AVATAR_URL_TEMPLATE = 'avatarUrlTemplate'
# 用户标识
USER_URL_TOKEN = 'urlToken'
# 用户名
USER_NAME = 'name'
# 用户自我介绍
USER_HEADLINE = 'headline'
# 用户居住地
USER_LOCATIONS = 'locations'
# 用户所在行业
USER_BUSINESS = 'business'
# 用户职业经历
USER_EMPLOYMENTS = 'employments'
# 用户教育经历
USER_EDUCATIONS = 'educations'
# 用户个人描述
USER_DESCRIPTION = 'description'
# 用户新浪微博 URL
USER_SINAWEIBO_URL = 'sinaWeiboUrl'
# 用户性别
USER_GENDER = 'gender'
# 正在关注用户的数目
USER_FOLLOWING_COUNT = 'followingCount'
# 关注者的数目
USER_FOLLOWER_COUNT = 'followerCount'
# 该用户回答问题的数目
USER_ANSWER_COUNT = 'answerCount'
# 用户提问数目
USER_QUESTION_COUNT = 'questionCount'
# 用户获得赞同的数目
USER_VOTE_UP_COUNT = 'voteupCount'

# JSON 数据关键字
JSON_ENTITIES = 'entities'
JSON_USERS = 'users'


# 解析 html 中的知乎用户信息
def parse_user_information(html_string, user_token):
    if html_string is None:
        return None
    # 提取 json 数据
    bs_object = BeautifulSoup(html_string, 'html.parser')
    data_string = bs_object.find('div', attrs={'id': 'data'})
    if data_string is None:
        return None
    else:
        data_string = data_string['data-state']

    # 字符串处理
    # 对转义 html 字符进行处理
    data_string = html.unescape(data_string)
    # 去除夹杂的 html 标签
    data_string = BeautifulSoup(data_string, 'html.parser').text
    # 转换为 json 对象
    try:
        # 防止解析到的 JSON 格式错误而引发异常
        json_data = json.loads(data_string)
    except ValueError:
        print('[error]解析到错误的 json 数据')
        return None

    # 提取实体
    if JSON_ENTITIES not in json_data:
        return None
    entities = json_data[JSON_ENTITIES]

    # 提取各个用户信息
    if JSON_USERS not in entities:
        return None
    users = entities[JSON_USERS]

    # 提取目标用户
    if user_token not in users:
        return None
    user = users[user_token]

    # 提取目标用户的个人信息
    avatarUrlTemplate = None
    urlToken = None
    name = None
    headline = None
    locations = []
    business = None
    employments = []
    educations = []
    description = None
    sinaWeiboUrl = None
    gender = None
    followingCount = None
    followerCount = None
    answerCount = None
    questionCount = None
    voteupCount = None

    if USER_AVATAR_URL_TEMPLATE in user:
        avatarUrlTemplate = user[USER_AVATAR_URL_TEMPLATE]

    if USER_URL_TOKEN in user:
        urlToken = user[USER_URL_TOKEN]

    if USER_NAME in user:
        name = user[USER_NAME]

    if USER_HEADLINE in user:
        headline = user[USER_HEADLINE]

    if USER_LOCATIONS in user:
        for location in user[USER_LOCATIONS]:
            locations.append(location['name'])

    if USER_BUSINESS in user:
        business = user[USER_BUSINESS]['name']

    if USER_EMPLOYMENTS in user:
        for employment in user[USER_EMPLOYMENTS]:
            elem = {}
            if 'job' in employment:
                job = employment['job']['name']
                elem.update({'job': job})
            if 'company' in employment:
                company = employment['company']['name']
                elem.update({'company': company})
            employments.append(elem)

    if USER_EDUCATIONS in user:
        for education in user[USER_EDUCATIONS]:
            if 'school' in education:
                school = education['school']['name']
                educations.append(school)

    if USER_DESCRIPTION in user:
        description = user[USER_DESCRIPTION]

    if USER_SINAWEIBO_URL in user:
        sinaWeiboUrl = user[USER_SINAWEIBO_URL]

    if USER_GENDER in user:
        gender = user[USER_GENDER]

    if USER_FOLLOWING_COUNT in user:
        followingCount = user[USER_FOLLOWING_COUNT]

    if USER_FOLLOWER_COUNT in user:
        followerCount = user[USER_FOLLOWER_COUNT]

    if USER_ANSWER_COUNT in user:
        answerCount = user[USER_ANSWER_COUNT]

    if USER_QUESTION_COUNT in user:
        questionCount = user[USER_QUESTION_COUNT]

    if USER_VOTE_UP_COUNT in user:
        voteupCount = user[USER_VOTE_UP_COUNT]

    # 构造用户信息实体
    user_info = {USER_AVATAR_URL_TEMPLATE: avatarUrlTemplate,
                 USER_URL_TOKEN: urlToken,
                 USER_NAME: name,
                 USER_HEADLINE: headline,
                 USER_LOCATIONS: locations,
                 USER_BUSINESS: business,
                 USER_EMPLOYMENTS: employments,
                 USER_EDUCATIONS: educations,
                 USER_DESCRIPTION: description,
                 USER_SINAWEIBO_URL: sinaWeiboUrl,
                 USER_GENDER: gender,
                 USER_FOLLOWING_COUNT: followingCount,
                 USER_FOLLOWER_COUNT: followerCount,
                 USER_ANSWER_COUNT: answerCount,
                 USER_QUESTION_COUNT: questionCount,
                 USER_VOTE_UP_COUNT: voteupCount}

    return user_info


# 解析 html 中的用户列表
def parse_user_list(html_string, user_token):
    if html_string is None:
        return None

    # 保存提取到的用户 url token
    user_token_list = []

    # 提取 json 数据
    bs_object = BeautifulSoup(html_string, 'html.parser')
    data_string = bs_object.find('div', attrs={'id': 'data'})['data-state']

    # 字符串处理
    # 对转义 html 字符进行处理
    data_string = html.unescape(data_string)
    # 去除夹杂的 html 标签
    data_string = BeautifulSoup(data_string, 'html.parser').text
    # 转换为 json 对象
    json_data = json.loads(data_string)

    # 提取实体
    if JSON_ENTITIES not in json_data:
        return None
    entities = json_data[JSON_ENTITIES]

    # 提取用户列表信息
    if JSON_USERS not in entities:
        return None
    users = entities[JSON_USERS]

    # 提取用户 token
    for token in users.keys():
        if token != user_token:
            user_token_list.append(token)

    return user_token_list


# 转换该用户信息实体为可保存的数据库格式
def convert_user_info(user_info):
    # 将居住地转换为‘；’分隔的字符串
    locations_string = ';'.join(str(x) for x in user_info[USER_LOCATIONS])
    user_info[USER_LOCATIONS] = locations_string

    # 将职业经历转换为‘XXX（XXX）’，并以‘；’ 分隔的字符串
    employments_list = []
    for employment in user_info[USER_EMPLOYMENTS]:
        temp = ''
        if 'company' in employment:
            temp += str(employment['company'])
        if 'job' in employment:
            temp += '-' + str(employment['job'])
        employments_list.append(temp)
    employments_string = ';'.join(str(x) for x in employments_list)
    user_info[USER_EMPLOYMENTS] = employments_string

    # 将教育经历转换为‘；’分隔的字符串
    educations_string = ';'.join(str(x) for x in user_info[USER_EDUCATIONS])
    user_info[USER_EDUCATIONS] = educations_string

    return user_info

# requestHeader = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#                  "Accept-Encoding": "gzip, deflate, sdch, br",
#                  "Accept-Language": "zh-CN,zh;q=0.8",
#                  "Cache-Control": "max-age=0",
#                  "Host": "www.zhihu.com",
#                  "Upgrade-Insecure-Requests": "1",
#                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
#
# if __name__ == '__main__':
#     session = requests.session()
#     session.headers = requestHeader
#     response = session.get('https://www.zhihu.com/people/excited-vczh/following?page=2')
    # print(parse_user_information(response.text, 'excited-vczh'))
    # print(parse_user_list(response.text, 'excited-vczh'))
    # print(convert_user_info(parse_user_information(response.text, 'excited-vczh')))
    # DBConnector.connection_init()
    # print(convert_user_info(parse_user_information(response.text, 'excited-vczh')))
    # DBConnector.add_user_info(convert_user_info(parse_user_information(response.text, 'excited-vczh')))
    # DBConnector.connection_init()