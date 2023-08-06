# coding:utf-8

# @Time: 2020/7/7 17:00
# @Auther: liyubin

import time
import paho.mqtt.client as mqtt
from super_sweetest.log import logger
from super_sweetest.keywords.mqtt import write_mqtt_msg

"""
mqtt client 非阻塞客户端 / 初始化MQTT客户端
"""


class MqttClient:

    def __init__(self, host, port, mqttClient):
        self._host = host
        self._port = port
        self._mqttClient = mqttClient

    def on_mqtt_connect(self, username, password):
        """非阻塞连接MQTT服务器"""
        self._mqttClient.tls_set()  # 配置网络加密和身份验证选项。启用S​​SL / TLS支持
        self._mqttClient.username_pw_set(username, password)
        self._mqttClient.connect_async(self._host, self._port, 60)
        self._mqttClient.loop_start()

    def on_subscribe(self, topic, qos):
        """订阅和消息回调"""
        self._mqttClient.subscribe(topic, qos)

    def on_unsubscribe(self, topic, qos):
        """ 取消订阅客户一个或多个主题"""
        self._mqttClient.unsubscribe(topic, qos)

    def on_publish(self, topic, msg, qos):
        """publish 发布消息"""
        self._mqttClient.publish(topic, msg, qos)

    def on_message_come(self, client, userdata, msg):
        """从服务器收到发布消息时的回调"""
        recv_msg = msg.payload.decode('utf-8')
        logger.info('Recv ---- 回调 topic 主题: ' + msg.topic + ' --------- 收到消息: ' + str(recv_msg))
        # 写入返回值（由于异常在mqtt回调函数中不会被抛出）
        write_mqtt_msg(recv_msg)

    def on_message(self):
        """消息回调"""
        self._mqttClient.on_message = self.on_message_come  # 调用 on_message_come 实际调用on_message

    def on_disconnect(self, client, userdata, rc):
        """断开"""
        if rc != 0:
            logger.info('Unexpected disconnection %s' % rc)

    def discionnect(self):
        """断开主方法"""
        self.on_disconnect(self._mqttClient, userdata=None, rc='')  # 调用 on_message_come 实际调用on_message


####################初始化MQTT客户端####################

class Mqtt_Init:

    def setup_mqttclient(self, _data):
        """
        初始化 类 MqttClient 客户端连接实例/通过实例调用MqttClient类方法
        """
        mqtt_host_ = _data.get('mqtt_host', 'no')
        mqtt_host = mqtt_host_.split(':')[0] if ":" in mqtt_host_ else 'no'
        mqtt_port = mqtt_host_.split(':')[1] if ":" in mqtt_host_ else 'no'
        client_Id = _data.get('client_Id', 'no')
        transport = _data.get('transport', 'no')
        mqtt_username = _data.get('mqtt_username', 'no')
        mqtt_password = _data.get('mqtt_password', 'no')
        # 参数key校验
        demo = {'mqtt_host': 'test.com:8443', 'client_Id': 'value',
                'transport': 'websockets/tcp', 'mqtt_username': 'value', 'mqtt_password': 'value'}
        assert 'no' not in (mqtt_host_, mqtt_host, mqtt_port, client_Id, transport, mqtt_username, mqtt_password)\
            , '\nmqtt 登录参数格式有误 \n当前参数：%s \n正确格式: %s' % (str(_data), str(demo))

        mqttClient = mqtt.Client(client_id=client_Id, clean_session=True, protocol=4, transport=transport)
        client = MqttClient(mqtt_host, int(mqtt_port), mqttClient)
        client.on_mqtt_connect(mqtt_username, mqtt_password)
        logger.info("--- Mqtt Connect Success ---")
        return client

    @staticmethod
    def teardown_mqttclient(client):
        """断开mqtt客户端连接"""
        client.discionnect()

#######################################################
