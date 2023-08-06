import asyncio
import queue
import sys
import threading
import time

import aiohttp
import requests

sys.path.insert(0, '../../frontiersman')
from frontiersman.gameboard.Board import *
from frontiersman.client.Gui import *
from frontiersman.client.Player import *
from frontiersman.main.GameLobby import *


class client:
    # def board_thread(self, board):
    #       self.client_instance.run(board)

    def __init__(self):
        self.enemy_list = []

    async def run(self, url, game_id, player_id, player_name, player_color, screen_num, lobby_obj, host=False):

        s = aiohttp.ClientSession()
        board_input = queue.Queue()
        board = Board()
        Color = player_color
        get_url = url + '/' + game_id + '/' + player_id + '/get'
        post_url = url + '/' + game_id + '/' + player_id + '/post'
        self.client_instance = Client(board_input, post_url, lobby_obj.window)
        self.client_instance.set_player(Player(player_name, Color, screen_num))
        lobby_obj.client_instance = self.client_instance
        lobby_obj.add_player(self.client_instance.player)
        # print(self.client_instance.player.name)
        for e in self.enemy_list:
            if (e not in lobby_obj.players):
                #print(e.name)
                lobby_obj.add_player(e)

        # Color = input('Choose a color: ')

        # print(get_url)

        async def send_message(message):
            await s.post(post_url, data={'msg': message})

        def get_longest_road():
            max_index = 0
            max_value = 0
            for i in range(0, len(self.client_instance.enemy_list)):
                if int(self.client_instance.enemy_list[i].longestRoad) > max_value:
                    max_index = i
                    max_value = int(self.client_instance.enemy_list[i].longestRoad)

            if (self.client_instance.player.get_longest_road(max_value)):
                self.client_instance.enemy_list[max_index].visibleVictoryPoints = str(
                    int(self.client_instance.enemy_list[max_index].visibleVictoryPoints) - 2)

        def get_largest_army():
            max_index = 0
            max_value = 0
            for i in range(0, len(self.client_instance.enemy_list)):
                if int(self.client_instance.enemy_list[i].largestArmy) > max_value:
                    max_index = i
                    max_value = int(self.client_instance.enemy_list[i].largestArmy)
            if (self.client_instance.player.get_largest_army(max_value)):
                self.client_instance.enemy_list[max_index].visibleVictoryPoints = str(
                    int(self.client_instance.enemy_list[max_index].visibleVictoryPoints) - 2)

        def player_hand_down(color):
            for en in self.enemy_list:
                if en.color == color:
                    en.handSize = str(int(en.handSize) - 1)

        while True:

            Response = await(await s.get(get_url)).text()
            if Response=='t':
                #print('timeout')
                continue
            # print('r', Response)
            # if Response == 'host':
            # num_players = self.get_valid_player_input("How many players(including you)? ")
            # add error checking from pakuri here
            #    ClientSocket.send(str.encode(str(num_players) + '\n'))

            if Response == "quit" or Response == "game not found":  # add more quit contigency!!!!
                #print(Response)
                #print("a player has disconnected")
                # self.client_instance.quit()
                lobby_obj.player_left = True
                await s.close()
                return
            elif Response == "leave":
                #print(Response)
                #print("host left")
                # self.client_instance.quit()
                lobby_obj.host_left = True
                await s.close()
                return
            elif Response == 'set':
                # xy=input("x,y: ")
                lobby_obj.client_instance.set_board_action("initialsettlement")
                coordinates = board_input.get()
                if coordinates == "quit":
                    continue
                board_input.task_done()
                settle = self.client_instance.building_locations.claimSettlement(int(coordinates.split(',')[0]),
                                                                                 int(coordinates.split(',')[1]), Color)
                self.client_instance.property_list.append(settle)
                self.client_instance.player.acquire_node(settle)
                port = self.client_instance.game_board.xy_give_port((settle.cord1, settle.cord2))
                # print(settle.cord1, settle.cord2)
                if port is not None:
                    self.client_instance.player.bankTrading.update(port.resource)
                self.client_instance.set_board_updated(True)
                await send_message(coordinates)
                await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
            
            elif Response == "startroad":
                self.client_instance.set_board_action("initialroad")
                coordinates = board_input.get()
                if coordinates == "quit":
                    continue
                board_input.task_done()
                # player.add
                road = self.client_instance.building_locations.claimRoad(int(coordinates.split(',')[0]),
                                                                         int(coordinates.split(',')[1]), Color)
                self.client_instance.road_list.append(road)
                self.client_instance.draw_road(road)
                self.client_instance.player.acquire_road(road)
                self.client_instance.set_board_updated(True)
                await send_message(coordinates)
                await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
            elif Response.split(',')[0] == "turnorder":
                col=Response.split(',')[1]
                self.client_instance.turn_player=col
                if col==Color:
                    self.client_instance.add_text("<b>Your Turn!</b>")
                else:
                    #print([e.name for e in self.client_instance.enemy_list])
                    for e in self.client_instance.enemy_list:
                        if e.color==col:
                            self.client_instance.add_text(e.name+"'s Turn!")
                self.client_instance.set_board_updated(True)
            elif Response.split(',')[0] == "set":
                # print("new settlement" + Response.split(',')[1] + Response.split(',')[1])
                self.client_instance.property_list.append(
                    self.client_instance.building_locations.claimSettlement(int(Response.split(',')[1]),
                                                                            int(Response.split(',')[2]),
                                                                            Response.split(',')[3]))
                self.client_instance.set_board_updated(True)
            elif Response.split(',')[0] == "road":
                # print("new road")
                # print("new settlement" + Response.split(',')[1] + Response.split(',')[1])
                road = self.client_instance.building_locations.claimRoad(int(Response.split(',')[1]),
                                                                         int(Response.split(',')[2]),
                                                                         Response.split(',')[3])
                self.client_instance.road_list.append(road)
                self.client_instance.draw_road(road)
                self.client_instance.set_board_updated(True)

            elif Response.split(',')[0] == "city":
                self.client_instance.building_locations.settlements[int(Response.split(',')[1])][
                    int(Response.split(',')[2])].city = True
                self.client_instance.set_board_updated(True)

                # print(Color)
            elif Response.split(',')[0] == "bank":
                arr = [int(x) for x in Response.split(',')[1:]]
                self.client_instance.bank.update(arr)
                self.client_instance.set_board_updated(True)

            elif Response.split('|')[0] == "board":
                number_list = [int(elem) for elem in Response.split('|')[1].split(',')]
                resource_list = Response.split('|')[2].split(',')
                port_list = Response.split('|')[3].split(',')
                board.generate_land(number_list, resource_list)
                board.generate_ports(port_list)
                self.client_instance.enemy_list = self.enemy_list
                self.client_instance.board_updated = True

            elif Response.split('|')[0] == "startgui":
                # threading.Thread(target=self.board_thread, args=(board,)).start()
                lobby_obj.board = board
                lobby_obj.run_game = True
                await s.post(post_url, data={'msg': "started"})
            elif Response == 'trade':
                self.client_instance.trade_cards_with_player(self.client_instance.trade_cost,
                                                             self.client_instance.trade_offer)
                await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
            elif Response == "getstart":
                # print("get starting resources")
                self.client_instance.start_resources()
                message = board_input.get()
                if message == "quit":
                    continue
                board_input.task_done()
                await send_message(message)
                await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                # bank_update = board_input.get()
                # board_input.task_done()
            elif Response == "steal":
                stolen_card = self.client_instance.stolen_card()
                self.client_instance.add_text("The Robber stole a "+stolen_card+ " from you!")
                await send_message('stolen,' + stolen_card)
                await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
            elif Response.split(',')[0] == "dice":
                roll = [int(x) for x in Response.split(',')[1:]]
                if sum(roll) == 7:
                    # self.client_instance.display_dice(roll)
                    continue
                # self.client_instance.display_dice(roll)
                self.client_instance.process_dice(sum(roll))
                message = board_input.get()
                if message == "quit":
                    continue
                board_input.task_done()
                await send_message(message)
                await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
            elif Response.split(',')[0] == "diceroll":
                roll = [int(x) for x in Response.split(',')[1:]]
                self.client_instance.is_rolling = True
                time.sleep(.5)
                self.client_instance.is_rolling = False
                if sum(roll) in [8,11]:
                    self.client_instance.add_text('An '+ str(sum(roll)) + ' was rolled.')
                else:
                    self.client_instance.add_text('A '+ str(sum(roll)) + ' was rolled.')
                self.client_instance.display_dice(roll)
                # await send_message('success')
            elif Response.split('|')[0] == "tradeoffer":
                offer = [int(i) for i in Response.split('|')[2].split(',')]
                cost = [int(i) for i in Response.split('|')[3].split(',')]
                # print(offer)
                # print(cost)
                self.client_instance.trade_offer = offer
                self.client_instance.trade_cost = cost
                self.client_instance.set_board_action('tradeoffer', 'display')
                message = board_input.get()
                if message == "quit":
                    continue
                board_input.task_done()
                await send_message(message)
                # self.client_instance.create_trade_prompt(offer, cost)
            elif Response == "discard":
                if self.client_instance.player.get_num_resources() < 8:
                    await send_message('noneed')
                else:
                    self.client_instance.set_board_action('discard', 'display')
                    message = board_input.get()
                    if message == "quit":
                        continue
                    board_input.task_done()
                    # print(message)
                    self.client_instance.pay_cards(self.client_instance.card_list_to_arr(message.split(',')))
                    message2 = board_input.get()
                    # print(message2)
                    if message2 == "quit":
                        continue
                    self.client_instance.set_board_updated(True)
                    await send_message(
                        Color + '|' + message2 + '|' + "enemyu," + self.client_instance.player.get_sent_to_enemies())
            elif Response == "turn" or Response == "robber":
                self.client_instance.turn_ended = False
                #self.client_instance.add_text("<b>Your Turn!</b>")
                self.client_instance.player.development_card_played = False
                self.client_instance.turn_start = True
                if Response == "robber":
                    self.client_instance.set_board_action("robber", 'turn')
                else:
                    self.client_instance.set_board_action("turn")

                while True:
                    message = board_input.get()
                    if message == "quit":
                        lobby_obj.player_left = True
                        await s.close()
                        return
                    elif message.split(',')[0] == "road":
                        road = self.client_instance.building_locations.claimRoad(int(message.split(',')[1]),
                                                                                 int(message.split(',')[2]), Color)
                        self.client_instance.road_list.append(road)
                        self.client_instance.draw_road(road)
                        self.client_instance.player.acquire_road(road)
                        get_longest_road()
                        self.client_instance.set_board_updated(True)
                        self.client_instance.pay_cards([1, 0, 1, 0, 0])
                        bank_up = board_input.get()
                        await send_message(bank_up)
                        board_input.task_done()
                        await send_message(message + ',' + Color)
                        await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                    elif (message.split(',')[0] == "robber"):
                        self.client_instance.game_board.set_robber(
                            (int(message.split(',')[1]), int(message.split(',')[2])))
                        # self.client_instance.player.get_largest_army(max([int(en.largestArmy) for en in self.client_instance.enemy_list], default=0))
                        get_largest_army()
                        self.client_instance.set_board_action('thieftarget', 'turn')
                        await send_message(message)
                        await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                    elif message.split('|')[0] == "tradeoffer":
                        self.client_instance.set_board_action('awaitingtrade')
                        await send_message(message)
                        Response2 = await(await s.get(get_url)).text()
                        while Response2 == 't':
                            Response2 = await(await s.get(get_url)).text()
                        if Response2 == "quit" or Response2 == "game not found":  # add more quit contigency!!!!
                            #print("a player has disconnected")
                            # self.client_instance.quit()
                            lobby_obj.player_left = True
                            await s.close()
                            return
                        ens = Response2.split(',')
                        if len(ens) == 1:
                            self.client_instance.add_text("Trade was Denied")
                            self.client_instance.set_board_action('turn', 'turn')
                        else:
                            ens.pop(0)
                            ens2 = []
                            for e in self.client_instance.enemy_list:
                                if e.color in ens:
                                    ens2.append(e)
                            self.client_instance.trade_list = ens2
                            self.client_instance.set_board_action('tradepartner', 'turn')
                            m2 = board_input.get()
                            if m2 == "quit":
                                lobby_obj.player_left = True
                                await s.close()
                                return
                            board_input.task_done()
                            if m2 != 'tradecancel':
                                await send_message(m2)
                                trade = [int(i) for i in message.split('|')[2].split(',')]
                                get = [int(i) for i in message.split('|')[3].split(',')]
                                self.client_instance.trade_cards_with_player(trade, get)
                                await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                                Response2 = await(await s.get(get_url)).text()
                                while Response2 == 't':
                                    Response2 = await(await s.get(get_url)).text()
                                if Response == "quit" or Response == "game not found":  # add more quit contigency!!!!
                                    #print("a player has disconnected")
                                    # self.client_instance.quit()
                                    lobby_obj.player_left = True
                                    await s.close()
                                    return
                                arr = Response2.split(',')[1:]
                                for en in self.client_instance.enemy_list:
                                    if en.color == arr[1]:
                                        en.update_enemy(arr)
                                # print(m2)
                            else:
                                await send_message(m2)
                            # print(ens2)
                    elif message.split(',')[0] == "steal":
                        await send_message(message)
                        card = await(await s.get(get_url)).text()
                        if card == "quit" or card == "game not found":  # add more quit contigency!!!!
                            #print("a player has disconnected")
                            # self.client_instance.quit()
                            lobby_obj.player_left = True
                            await s.close()
                            return
                        if card.split(',')[1] == "none":
                            pass
                            #print("no cards to steal")
                        else:
                            self.client_instance.add_text("You stole a "+card.split(',')[1])
                            self.client_instance.steal_card(card.split(',')[1])
                            player_hand_down(message.split(',')[1])
                            self.client_instance.set_board_action('turn')
                            # self.client_instance.set_player_info(self.client_instance.player, self.client_instance.enemy_list)
                        await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                    elif message.split(',')[0] == "set":
                        settle = self.client_instance.building_locations.claimSettlement(int(message.split(',')[1]),
                                                                                         int(message.split(',')[2]),
                                                                                         Color)
                        self.client_instance.property_list.append(settle)
                        self.client_instance.player.acquire_node(settle)
                        port = self.client_instance.game_board.xy_give_port((settle.cord1, settle.cord2))
                        if port is not None:
                            self.client_instance.player.bankTrading.update(port.resource)
                        self.client_instance.set_board_updated(True)
                        self.client_instance.pay_cards([1, 1, 1, 0, 1])
                        bank_up = board_input.get()
                        await send_message(bank_up)
                        board_input.task_done()
                        await send_message(message + ',' + Color)
                        await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                    elif message == "dev" and Actions.buy_development_check(self.client_instance.player):
                        await send_message(message)
                        card = await(await s.get(get_url)).text()
                        # print(card)
                        self.client_instance.get_dev_card(card)
                        self.client_instance.player.developmentHand.add_card(card)
                        if card == 'victoryPoint':
                            self.client_instance.player.hiddenVictoryPoints += 1
                        self.client_instance.pay_cards([0, 1, 0, 1, 1])
                        await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                    elif message.split(',')[0] == "monopoly":
                        await send_message(message)
                        await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                    elif message.split(',')[0] == "city":
                        settle = self.client_instance.building_locations.settlements[int(message.split(',')[1])][
                            int(message.split(',')[2])].city = True
                        self.client_instance.player.acquire_city()
                        self.client_instance.set_board_updated(True)
                        self.client_instance.pay_cards([0, 2, 0, 3, 0])
                        bank_up = board_input.get()
                        await send_message(bank_up)
                        board_input.task_done()
                        await send_message(message)
                        await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                    elif message == "end":
                        # print("end")
                        if (
                                self.client_instance.player.victoryPoints + self.client_instance.player.hiddenVictoryPoints >= 10):
                            await send_message('winner,' + self.client_instance.player.get_sent_to_enemies())
                            # ClientSocket.send(str.encode('winner,' + self.client_instance.player.name + '\n'))
                        else:
                            await send_message(message)
                            await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                        break
                    elif message.split(',')[0] == "bank":
                        await send_message(message)
                        await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())

                    elif message == "roadroad":
                        board_input.task_done()
                        if len(Actions.build_road_available(self.client_instance.player, True)) > 0:
                            self.client_instance.set_board_action("roadfree", 'turn')
                            message = board_input.get()
                            if message == "quit":
                                lobby_obj.player_left = True
                                await s.close()
                                return
                            board_input.task_done()
                            road = self.client_instance.building_locations.claimRoad(int(message.split(',')[1]),
                                                                                     int(message.split(',')[2]), Color)
                            self.client_instance.road_list.append(road)
                            self.client_instance.draw_road(road)
                            self.client_instance.player.acquire_road(road)
                            get_longest_road()
                            self.client_instance.set_board_updated(True)
                            await send_message(message + ',' + Color)
                            await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                        if len(Actions.build_road_available(self.client_instance.player, True)) > 0:
                            self.client_instance.set_board_action("roadfree", 'turn')
                            message = board_input.get()
                            if message == "quit":
                                lobby_obj.player_left = True
                                await s.close()
                                return
                            board_input.task_done()
                            road = self.client_instance.building_locations.claimRoad(int(message.split(',')[1]),
                                                                                     int(message.split(',')[2]), Color)
                            self.client_instance.road_list.append(road)
                            self.client_instance.draw_road(road)
                            self.client_instance.player.acquire_road(road)
                            get_longest_road()
                            self.client_instance.set_board_updated(True)
                            await send_message(message + ',' + Color)
                            await send_message("enemyu," + self.client_instance.player.get_sent_to_enemies())
                board_input.task_done()

                # while turn:
            elif Response.split(',')[0] == "robber":
                self.client_instance.game_board.set_robber((int(Response.split(',')[1]), int(Response.split(',')[2])))
                self.client_instance.set_board_updated(True)
            elif Response.split(',')[0] == "monopoly":
                self.client_instance.pay_monopoly(Response.split(',')[1])
                self.client_instance.set_board_updated(True)
            elif Response == "notturn":
                self.client_instance.set_board_action("display", 'display')
            # elif Response.split(',')[0] == "enemy":
            # self.enemy_list.append(EnemyPlayer(Response.split(',')[1], Response.split(',')[2]))
            # print(Response.split(',')[1], "(" + Response.split(',')[2] + ")", "has joined")
            elif Response.split(',')[0] == "enemy":
                e = EnemyPlayer(Response.split(',')[1], Response.split(',')[2])
                if (e not in lobby_obj.players):
                    # print(e.name)
                    lobby_obj.add_player(e)
                if (e not in self.enemy_list):
                    self.enemy_list.append(e)
            elif Response.split(',')[0] == "enemyleave":
                for e in self.enemy_list:
                    if e.color == Response.split(',')[1]:
                        lobby_obj.remove_player(e)
                        self.enemy_list.remove(e)
                        # print(self.enemy_list)
            elif Response.split(',')[0] == "enemyu":
                arr = Response.split(',')[1:]
                for en in self.client_instance.enemy_list:
                    if en.color == arr[1]:
                        en.update_enemy(arr)
                        self.client_instance.player.lose_longest_road(int(en.longestRoad))
                        self.client_instance.player.lost_largest_army(int(en.largestArmy))
            elif Response.split(',')[0] == "winner":
                if (Response.split(',')[2] == self.client_instance.player.color):
                    lobby_obj.winner = 'You'
                else:
                    lobby_obj.winner = Response.split(',')[1]

                self.client_instance.running = False  # add a victory screen also need to send who won
                lobby_obj.to_menu = True
                await s.close()
                return
            elif Response != "":
                # print(Response.split(',')[0])
                pass

            # while True:
            # Input = input('Say Something: ')
            # ClientSocket.send(str.encode(Input))
            # Response = ClientSocket.recv(1024)
            # print(Response.decode('utf-8'))
            # roadMap.printAllSettlements()
            # roadMap.printAllRoads()
        # self.client_instance.quit()

        lobby_obj.to_menu = True
        return


def game_thread_run(client, url, game_code, player_code, name, color, screen_num, window, host):
    try:
        asyncio.run(client.run(url, game_code, player_code, name, color, screen_num, window, host))
    except RuntimeError:
        pass


def main():
    if os.path.dirname(__file__) != '':
        os.chdir(os.path.dirname(__file__))
    # os.chdir(os.path.dirname(__file__))
    if len(sys.argv) == 2 and sys.argv[1] == "remote":
        url = 'https://frontiersman.herokuapp.com'
    else:
        url = 'http://127.0.0.1:5000'
    s = requests.Session()
    host = False

    def create_game(lobby_obj):
        host = True
        try:
            r = s.post(url + '/create', data={'name': lobby_obj.name})
            try:
                name = lobby_obj.name
                # print(r.text)
                response = r.text.split(',')
                game_code = response[0]
                lobby_obj.set_lobby_code(game_code)
                player_code = response[1]
                lobby_obj.player_code = player_code
                lobby_obj.color = response[2]
                lobby_obj.screen_num = response[3]
                try:
                    threading.Thread(
                        target=game_thread_run, args=(client(), url, game_code, player_code, name, lobby_obj.color,
                                                      lobby_obj.screen_num, lobby_obj, lobby_obj.is_host)).start()
                except RuntimeError:
                    pass
                    print('thread\'s dead , baby, thread is dead')
                
            except:
                #pass
                print('non-post related error')
        except:
            lobby_obj.create_notification(['Server Creation Failed', 'Can not reach server'], True)
            return False
        finally:
            # close threads opened during try
            pass
        return True

    def join_game(lobby_obj):
        host = False
        data = {'name': lobby_obj.name}
        # name=lobby_obj.name
        try:
            r = s.post(url + '/join/' + lobby_obj.lobby_code, data=data)
        except:
            return 'fail'
        # print(url + '/join/' + lobby_obj.lobby_code)
        if r.text == "game not found":
            #print("failed to join")  # add popup later
            return 'code'
        elif r.text == 'game already started':
            return 'running'
        game_code = lobby_obj.lobby_code
        # print(r.text)
        # print(lobby_obj.players)
        response = r.text.split('|')
        player_code = response[0].split(',')[0]
        lobby_obj.player_code = player_code
        lobby_obj.color = response[0].split(',')[1]
        lobby_obj.screen_num = response[0].split(',')[2]
        cli = client()
        for x in range(1, len(response)):
            # addplayers
            cli.enemy_list.append(EnemyPlayer(response[x].split(',')[0], response[x].split(',')[1]))
            # print(response[x].split(',')[0], response[x].split(',')[1])
        try:
            threading.Thread(target=game_thread_run, args=(
                cli, url, game_code, player_code, lobby_obj.name, lobby_obj.color, lobby_obj.screen_num, lobby_obj,
                lobby_obj.is_host)).start()
        except RuntimeError:
            #pass
            print('thread\'s dead , baby, thread is dead')
        return 'success'

    def leave_lobby(lobby_obj):
        post_url = url + '/' + lobby_obj.lobby_code + '/' + lobby_obj.player_code + '/post'
        r = s.post(post_url, data={'msg': 'leave'})
        lobby_obj.players = []
        lobby_obj.lobby_status = []

    def start(lobby_obj):
        lobby_obj.loading = True
        post_url = url + '/' + lobby_obj.lobby_code + '/' + lobby_obj.player_code + '/post'
        r = s.post(post_url, data={'msg': 'start'})
        lobby_obj.loading = False

    def host_leave_lobby(name):
        r = s.post(url + '/create', data={'name': name})
        # print(r.text)
        response = r.text.split(',')
        game_code = response[0]
        player_code = response[1]
        color = response[2]
        screen_num = response[3]
    try:
        test = GameLobby(RESOLUTION, callbacks=[create_game, join_game, leave_lobby, start])
    except TypeError as a:
        try:
            test.to_menu=True
        except UnboundLocalError:
            print(a)

if __name__ == "__main__":
    main()
