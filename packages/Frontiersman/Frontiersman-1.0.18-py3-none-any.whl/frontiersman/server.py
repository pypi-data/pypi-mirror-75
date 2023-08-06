import asyncio
import os
import queue
import random
import threading

from aiohttp import web

loop = asyncio.get_event_loop()
running_games = {}
chars = ['2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K',
         'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e',
         'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def make_code(length, existing_list):
    code = ''
    for i in range(0, length):
        code = code + random.choice(chars)
    if code in existing_list:
        code = make_code(length, existing_list)
    else:
        return code


def game_over(code):
    try:
        del running_games[code]
        print(running_games.keys())
    except KeyError:
        print('Key', code, 'not found')


class client:
    def __init__(self, name, id2, host):
        self.name = name
        self.id = id2
        self.color = ''
        self.is_host = host
        self.queue = asyncio.Queue()

    def set_data(self, color, screen_num):
        self.color = color
        self.screen_num = screen_num


# from frontiersman.client import ClientHelper
class ServerThread:

    def __init__(self, code):
        self.code = code
        self.player_count = 0
        self.game_code = code
        self.players = {}
        self.started = False
        self.winner = False
        self.queue = queue.Queue()
        self.color_list = ['red', 'cyan', 'orange', 'blue', 'green', 'pink', 'yellow']
        random.shuffle(self.color_list)
        self.resource_list = ['Wheat'] * 4 + \
                             ['Sheep'] * 4 + \
                             ['Ore'] * 3 + \
                             ['Brick'] * 3 + \
                             ['Wood'] * 4 + \
                             ['Desert'] * 1
        self.number_list = [2, 12]
        for index in range(3, 12):
            if index == 7:
                pass
            else:
                self.number_list.append(index)
                self.number_list.append(index)
        self.port_list = ['Wheat'] + \
                         ['Sheep'] + \
                         ['Ore'] + \
                         ['Brick'] + \
                         ['Wood'] + \
                         ['None'] * 4
        self.developmentDeck = ['knight'] * 15 + \
                               ['roadBuilding'] * 2 + \
                               ['yearOfPlenty'] * 2 + \
                               ['monopoly'] * 2 + \
                               ['victoryPoint'] * 5
        random.shuffle(self.developmentDeck)
        random.shuffle(self.number_list)
        random.shuffle(self.resource_list)
        random.shuffle(self.port_list)
        # asyncio.run(self.run())

    def add_player(self, player_object):
        player_object.set_data(self.color_list.pop(0), self.player_count)
        self.players[player_object.id] = player_object
        self.player_count += 1

    def run(self):
        asyncio.run(self.async_run())

    def handle_incoming(self, message):
        self.queue.put(message)

    def game_over(self):
        self.winner = True

    async def async_run(self):

        def dice_roll():
            return str(random.randint(1, 6)) + ',' + str(random.randint(1, 6))

        async def sendtoall(message):
            for key in self.players:
                asyncio.run_coroutine_threadsafe(self.players[key].queue.put(message), loop)

        async def sendtoallButOne(message, cli_code):
            for key in self.players:
                if key != cli_code:
                    asyncio.run_coroutine_threadsafe(self.players[key].queue.put(message), loop)

        async def sendtoOne(message, cli_code):
            asyncio.run_coroutine_threadsafe(self.players[cli_code].queue.put(message), loop)

        def readfromBuffer():
            while self.queue.empty():
                continue
            msg = self.queue.get()
            self.queue.task_done()
            #print("test", msg)
            return msg

        def get_key_from_color(color):
            for key in self.players.keys():
                if self.players[key].color == color:
                    return key

        async def quit():
            for key in keyorder:
                await sendtoall("quit")  # turn this into who won for the victory screen, obv
            game_over(self.code)

        # board randomizer

        numberstring = 'board|' + ','.join([str(elem) for elem in self.number_list]) + '|' + ','.join(
            self.resource_list) + '|' + ','.join(self.port_list)
        await sendtoall(numberstring)
        keyorder = list(self.players.keys())
        # for key in keyorder:
        # await sendtoallButOne("enemy," + self.players[key].name + "," + self.players[key].color, key)
        for key in keyorder:
            # cli.socket.send(str.encode("startgui\n"))
            await sendtoOne("startgui", key)
            message = readfromBuffer()
            if message == "quit":
                await quit()
                return

        # setup

        random.shuffle(keyorder)
        for key in keyorder:
            await sendtoall('turnorder,'+self.players[key].color)
            await sendtoOne("set", key)
            # print("test")
            coordinates = readfromBuffer()
            # print(coordinates)
            if coordinates == "quit":
                await quit()
                return
            await sendtoallButOne("set," + coordinates + "," + self.players[key].color, key)
            message = readfromBuffer()
            if message == "quit":
                await quit()
                return
            await sendtoallButOne(message, key)
            await sendtoOne("startroad", key)
            coordinates = readfromBuffer()
            if coordinates == "quit":
                await quit()
                return
            await sendtoallButOne("road," + coordinates + "," + self.players[key].color, key)
            message = readfromBuffer()
            if message == "quit":
                await quit()
                return
            await sendtoallButOne(message, key)

        for key in reversed(keyorder):
            await sendtoall('turnorder,'+self.players[key].color)
            await sendtoOne("set", key)
            coordinates = readfromBuffer()
            if coordinates == "quit":
                await quit()
                return
            await sendtoallButOne("set," + coordinates + "," + self.players[key].color, key)
            message = readfromBuffer()
            if message == "quit":
                await quit()
                return
            await sendtoallButOne(message, key)
            await sendtoOne("startroad", key)
            coordinates = readfromBuffer()
            if coordinates == "quit":
                await quit()
                return
            await sendtoallButOne("road," + coordinates + "," + self.players[key].color, key)
            message = readfromBuffer()
            if message == "quit":
                await quit()
                return
            await sendtoallButOne(message, key)

        for key in keyorder:
            await sendtoOne('getstart', key)
            message = readfromBuffer()
            if message == "quit":
                await quit()
                return
            await sendtoallButOne(message, key)
            message = readfromBuffer()
            if message == "quit":
                await quit()
                return
            await sendtoallButOne(message, key)
        while not self.winner:
            for key in keyorder:
                await sendtoall('turnorder,'+self.players[key].color)
                dice = dice_roll()
                for key2 in keyorder:
                    await sendtoOne('diceroll,' + dice, key2)
                if int(dice.split(',')[0]) + int(dice.split(',')[1]) == 7:
                    await sendtoall('dice,' + dice)
                    await sendtoall('discard')
                    for x in range(0, len(keyorder)):
                        message = readfromBuffer()
                        if message == "quit":
                            await quit()
                            return
                        if message == "noneed":
                            continue
                        else:
                            res = message.split('|')
                            key4 = get_key_from_color(res[0])
                            await sendtoallButOne(res[1], key4)
                            await sendtoallButOne(res[2], key4)
                else:
                    # await sendtoall('diceroll,' + dice)
                    for key2 in keyorder:
                        await sendtoOne('dice,' + dice, key2)
                        # print('dice,' + dice, key2)
                        message = readfromBuffer()
                        if message == "quit":
                            await quit()
                            return
                        await sendtoallButOne(message, key2)
                        message = readfromBuffer()
                        if message == "quit":
                            await quit()
                            return
                        await sendtoallButOne(message, key2)
                if int(dice.split(',')[0]) + int(dice.split(',')[1]) == 7:
                    await sendtoOne("robber", key)
                else:
                    await sendtoOne("turn", key)
                while True:
                    message = readfromBuffer()
                    if message == "quit":
                        await quit()
                        return
                    # #print(message)
                    if message == "end":
                        message = readfromBuffer()
                        if message == "quit":
                            await quit()
                            return
                        await sendtoallButOne(message, key)
                        break
                    elif message.split(',')[0] == "winner":
                        self.winner = True
                        await sendtoall(message)
                        # #print(message)
                        break
                    elif message.split('|')[0] == "tradeoffer":
                        await sendtoallButOne(message, key)
                        trade_list = 'tradewith'
                        for x in range(0, len(keyorder) - 1):
                            message = readfromBuffer()
                            if message == "quit":
                                await quit()
                                return
                            if message.split(',')[0] == "deny":
                                continue
                            elif message.split(',')[0] == "accept":
                                trade_list += ',' + message.split(',')[1]
                        await sendtoOne(trade_list, key)
                        if trade_list != 'tradewith':
                            message = readfromBuffer()
                            if message == "quit":
                                await quit()
                                return
                            if message != 'tradecancel':
                                await sendtoOne("trade", get_key_from_color(message.split(',')[1]))
                                message = readfromBuffer()
                                if message == "quit":
                                    await quit()
                                    return
                                await sendtoallButOne(message, get_key_from_color(message.split(',')[2]))
                                message = readfromBuffer()
                                if message == "quit":
                                    await quit()
                                    return
                                await sendtoallButOne(message, get_key_from_color(message.split(',')[2]))
                            else:
                                await sendtoallButOne(message, key)
                    elif message.split(',')[0] == 'steal':
                        for key2 in self.players.keys():
                            if self.players[key2].color == message.split(',')[1]:
                                await sendtoOne('steal', key2)
                                stolen_message = readfromBuffer()
                                if stolen_message == "quit":
                                    await quit()
                                    return
                                enemy_update = readfromBuffer()
                                if enemy_update == "quit":
                                    await quit()
                                    return
                                await sendtoOne(stolen_message, key)
                                for key3 in self.players.keys():
                                    if key3 != key2 and key3 != key:
                                        await sendtoOne(enemy_update, key3)
                    elif message == "dev":
                        card = self.developmentDeck.pop(0)
                        await sendtoOne(card, key)
                    else:
                        await sendtoallButOne(message, key)
                await sendtoOne("notturn", key)
                # message=readfromBuffer(cli.socket)
                # #print(message)
                # await sendtoallButOne(message, cli)

        # game loop
        for key in keyorder:
            await sendtoall("quit")  # turn this into who won for the victory screen, obv
        game_over(self.code)

    '''
    except(ConnectionResetError):
        {
            #print("A player has disconnected")
        }
    '''


async def join(request):
    data = await request.post()
    code = request.match_info.get('game_id', "fail")
    if code == "fail" or code not in running_games.keys():
        return web.Response(text="game not found")
    else:
        # players=running_games
        if not running_games[code].started:
            player_code = make_code(15, running_games[code].players.keys())
            running_games[code].add_player(client(data['name'], player_code, False))
            enemystring = ''
            for key in running_games[code].players.keys():
                if key != player_code:
                    asyncio.run_coroutine_threadsafe(running_games[code].players[key].queue.put(
                        "enemy," + data['name'] + "," + running_games[code].players[player_code].color), loop)
                    enemystring += '|' + running_games[code].players[key].name + ',' + running_games[code].players[
                        key].color
            return web.Response(text=player_code + ',' + running_games[code].players[player_code].color + ',' + str(
                running_games[code].players[player_code].screen_num) + enemystring)
        else:
            return web.Response(text='game already started')


async def make_game(request):
    data = await request.post()
    game_code = make_code(5, running_games.keys())
    player_code = make_code(15, [])
    running_games[game_code] = ServerThread(game_code)
    running_games[game_code].add_player(client(data['name'], player_code, True))
    return web.Response(
        text=game_code + ',' + player_code + ',' + running_games[game_code].players[player_code].color + ',' + str(
            running_games[game_code].players[player_code].screen_num))


async def get_from_queue(code, player_code):
    msg = await running_games[code].players[player_code].queue.get()
    return msg


async def get_data(request):
    code = request.match_info.get('game_id', "fail")
    if code == "fail" or code not in running_games.keys():
        return web.Response(text="game not found")
    player_code = request.match_info.get('player_id', "fail")
    if player_code == "fail" or player_code not in running_games[code].players.keys():
        return web.Response(text="player not found")
    try:
        msg = await asyncio.wait_for(get_from_queue(code, player_code), timeout=10.0)
    except asyncio.TimeoutError:
        return web.Response(text='t')
    return web.Response(text=msg)


async def kill_all_games(request):
    data = await request.post()
    if data['code'] == 'double_snap':
        running_games.clear()


async def game_update(request):
    data = await request.post()
    code = request.match_info.get('game_id', "fail")
    if code == "fail" or code not in running_games.keys():
        return web.Response(text="game not found")
    player_code = request.match_info.get('player_id', "fail")
    if player_code == "fail" or player_code not in running_games[code].players.keys():
        return web.Response(text="player not found")
    #
    # print('data is', data['msg'])
    if data['msg'] == "start":
        if running_games[code].players[player_code].is_host and not running_games[code].started:
            # print('send:', data['msg'])
            threading.Thread(target=running_games[code].run, ).start()
            running_games[code].started = True
        else:
            web.Response(text="you're a cheater")
    elif data['msg'] == "prestart":
        if not running_games[code].started:
            for key in running_games[code].players.keys():
                asyncio.run_coroutine_threadsafe(running_games[code].players[key].queue.put("closelisten"), loop)
    elif data['msg'] == "leave":
        color = running_games[code].players[player_code].color
        if running_games[code].players[player_code].is_host:
            for key in running_games[code].players.keys():
                asyncio.run_coroutine_threadsafe(running_games[code].players[key].queue.put("leave"), loop)
            game_over(code)
        else:
            for key in running_games[code].players.keys():
                if key != player_code:
                    asyncio.run_coroutine_threadsafe(running_games[code].players[key].queue.put("enemyleave," + color),
                                                     loop)
            asyncio.run_coroutine_threadsafe(running_games[code].players[player_code].queue.put("quit"), loop)
            del running_games[code].players[player_code]
            running_games[code].color_list.append(color)
            # print(running_games[code].players.keys())
    elif data['msg'] == "quit":
        #for key in running_games[code].players.keys():
            #asyncio.run_coroutine_threadsafe(running_games[code].players[key].queue.put("quit"), loop)
        running_games[code].handle_incoming(data['msg'])

    else:
        running_games[code].handle_incoming(data['msg'])
    return web.Response(text="sucessful post")


# def hello(request):
def main():
    app = web.Application()
    app.router.add_route('POST', '/create', make_game)
    app.router.add_route('POST', '/join/{game_id}', join)
    app.router.add_route('GET', '/{game_id}/{player_id}/get', get_data)
    app.router.add_route('POST', '/{game_id}/{player_id}/post', game_update)
    app.router.add_route('POST', '/killgames', kill_all_games)
    f = loop.create_server(app.make_handler(), '0.0.0.0', os.environ.get('PORT', '5000'))
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
