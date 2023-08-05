============
PPNetwork
============
***************
简介
***************

    PPNetwork 是无中心节点的网络驱动，可以在任何环境下建立数据连接。

    PPNetwork采用UDP，自动寻找同类节点，并自动寻找到目标地址的路径，发送数据。

    至少需要添加一个初始的对等节点。可以通过对等节点获得其邻居信息，逐渐扩大自己的网络。上层应用可以通过寻找好友的方式添加对等节点。

****
安装
****
::

  pip install py-ppnet


****
使用
****

ppnetwork 不能独立运行，需要根据接口，开发上层应用。
需要至少一个可访问到的peer节点，可以通过配置也可以在运行时动态增加。

config模式
**********

config.yaml::

    node_port: 54320
    nodes: [["172.31.102.109",54320]]

程序代码::

    from ppnet import PPNetNode

    ppnetnode = PPNetNode(config=config)
    ppnetnode.start()
    ppnetnode.send(data,addr1)
    data,addr2 = ppnetnode.receive(count)
    ...
    ppnetnode.quit()


动态增加模式
************
程序代码::

 from ppnet import PPNetNode

 ppnetnode = PPNetNode(node_port=54320)
 ppnetnode.set_peer(addr)
 ppnetnode.start()
 ppnetnode.send(data,addr1)
 data,addr2 = ppnetnode.receive(count)
 ...
 ppnetnode.quit()

