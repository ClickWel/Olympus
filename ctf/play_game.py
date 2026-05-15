import socket
import time

def play_game():
    s = socket.socket()
    s.settimeout(10)
    s.connect(('154.57.164.78', 32230))
    
    # Receive welcome message
    data = s.recv(4096).decode('utf-8', errors='ignore')
    print(data)
    
    # Send 'y' to start
    s.send(b'y\n')
    time.sleep(0.5)
    
    # Game loop - try 500 rounds
    for i in range(500):
        data = s.recv(4096).decode('utf-8', errors='ignore')
        
        # Check if we got the flag
        if 'HTB{' in data:
            print(f"\n*** FLAG FOUND IN ROUND {i+1}: {data.strip()} ***")
            break
        
        # Check if this is a question
        if 'What do you do?' in data or 'GORGE' in data or 'PHREAK' in data or 'FIRE' in data:
            # Parse the scenario
            lines = data.strip().split('\n')
            scenario_line = ''
            for line in lines:
                if 'GORGE' in line or 'PHREAK' in line or 'FIRE' in line:
                    scenario_line = line.strip()
                    break
            
            if not scenario_line:
                for word in ['GORGE', 'PHREAK', 'FIRE']:
                    idx = data.find(word)
                    if idx != -1:
                        scenario_line = data[idx:].split('\n')[0].strip()
                        break
            
            # Parse comma-separated scenarios
            response_parts = []
            parts = [p.strip() for p in scenario_line.split(',')]
            for part in parts:
                if 'GORGE' in part:
                    response_parts.append('STOP')
                elif 'PHREAK' in part:
                    response_parts.append('DROP')
                elif 'FIRE' in part:
                    response_parts.append('ROLL')
            
            response = '-'.join(response_parts)
            s.send((response + '\n').encode())
            time.sleep(0.2)
    
    s.close()
    print("Game ended - no flag found in 500 rounds")

if __name__ == '__main__':
    play_game()
