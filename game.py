import constants


class AgentWrapper(object):
    """
    Wrapper for agent instances that is aware of its position in the maze.
    """
    def __init__(self, maze, agent, x, y):
        self.maze = maze
        self.agent = agent
        self.x = x
        self.y = y

        self._offset_x = x
        self._offset_y = y

    def act(self):  # TODO: sanitize sanitize sanitize
        """
        Poll the agent for the direction to move, then move him in that
        direction.
        """
        result = self.agent.act()
        dir_lookup = {
            constants.UP: (0, -1),
            constants.RIGHT: (1, 0),
            constants.DOWN: (0, 1),
            constants.LEFT: (-1, 0),
            None: (0, 0),
        }
        nx, ny = map(sum, zip(dir_lookup[result], (self.x, self.y)))
        if self.maze.is_wall(nx, ny):
            return False
        self.x, self.y = nx, ny

    def see(self, information):
        """
        Since the agent doesn't know where he started, convert the
        coordinates into something he can understand.
        """
        information = {
            (x - self._offset_x, y - self._offset_y, direction): wall
            for (x, y, direction), wall in information.iteritems()
        }
        return self.agent.see(information)


class Game(object):
    def __init__(self, agent_cls, maze_cls, num_agents, width, height):
        # self.maze = board.RectangleLabyrinth(width, height)
        self.maze = maze_cls(width, height)
        self.agents = [  # TODO: distribute this to prevent bullshit
            AgentWrapper(self.maze, agent_cls(), x, y)
            for x, y in [
                (27, 27), (37, 27)  # TODO: place these more intelligently
            ][:num_agents]
        ]

    def reveal_sight(self):
        for agent in self.agents:
            agent.see({
                (agent.x, agent.y, direction): self.maze.is_wall(agent.x, agent.y, direction)
                for direction in constants.DIRECTIONS
            })

    def query_actions(self):
        for agent in self.agents:
            agent.act()

    def game_loop(self):
        while 1:
            self.reveal_sight()
            # print self.agents[0].agent  # What the agent sees
            print self  # The entire game overview
            raw_input()
            self.query_actions()

    def __str__(self):
        maze = self.maze
        agent_coords = set((agent.x, agent.y) for agent in self.agents)
        string = []
        for y in xrange(maze.top, maze.bottom + 1):
            for x in xrange(maze.left, maze.right + 1):
                wall = maze.walls.get((x, y))
                if (x, y) in agent_coords:
                    string.append("0")
                elif wall is None:
                    string.append(" ")
                else:
                    string.append("#" if wall else ".")
            string.append("\n")
        return ''.join(string)
