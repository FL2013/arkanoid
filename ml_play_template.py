"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False  #play ball or not
    
    ball_x0=ball_x1=0
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()
    ball_x1=comm.get_scene_info().ball[0]
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False
            ball_x1=scene_info.ball[0]
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
            
        ball_x0=ball_x1
        ball_x1=scene_info.ball[0]
        ball_height = 400-scene_info.ball[1]
        
        if ball_x1 > ball_x0 :
             ball_endx = scene_info.ball[0] + ball_height
        else :
             ball_endx = scene_info.ball[0] - ball_height
             
        if  ball_endx > 200 :
            ball_endx = 400 - ball_endx 
        elif ball_endx < 0 :
            ball_endx = -1 * ball_endx
            
            
        
       
                
            
        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)  #RIGHT  NONE
            ball_served = True
        elif ball_endx > scene_info.platform[0] + 36 :
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        elif ball_endx < scene_info.platform[0] +4 :
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            
