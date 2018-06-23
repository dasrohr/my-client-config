
# |::::::::::::: oh-my-zsh ::::::::::::::>>>
# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh
# Auto Update Enable
DISABLE_AUTO_UPDATE="true"
# Default Theme
POWERLEVEL9K_MODE='awesome-fontconfig'
ZSH_THEME="powerlevel9k/powerlevel9k"
# Active plugins
plugins=(git themes pip node npm history-substring-search zsh-syntax-highlighting)

source $ZSH/oh-my-zsh.sh

export PATH="$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games"

# Add RVM to PATH for scripting
export PATH="$PATH:$HOME/.rvm/bin"

export PATH=~/.npm-global/bin:$PATH

# export LC_TYPE="en_US.UTF-8"
# export LC_ALL="en_US.UTF-8"
# |::::::::::::: oh-my-zsh ::::::::::::::<<<
# |::::::::::::: zsh git prompt ::::::::::::::>>>
source $HOME/.zsh-git-prompt/zshrc.sh
if [[ $EUID -ne 0 ]]; then
# no root
PROMPT='
%{$fg_no_bold[black]%}%~  $(git_super_status)
%{$fg_bold[green]%}· %{$fg_bold[yellow]%}· %{$fg_bold[red]%}· '
RPROMPT='%{$reset_color%} ⌚ %T %{$fg_no_bold[black]%}|%n @ %m|%{$reset_color%}'
else
# root
PROMPT='
%{$fg_no_bold[black]%}%~  $(git_super_status)
%{$fg_bold[green]%}• %{$fg_bold[yellow]%}• %{$fg_bold[red]%}• %{$fg_bold[red]%} # '
RPROMPT='%{$reset_color%} ⌚ %T %{$fg_no_bold[black]%}|%n @ %m|%{$reset_color%}'
fi
# |::::::::::::: zsh git prompt ::::::::::::::<<<

# theme settings
# custom_wifi_signal)
# POWERLEVEL9K_CUSTOM_WIFI_SIGNAL="echo signal: \$(nmcli device wifi | grep yes | awk '{print \$8}')"
# POWERLEVEL9K_CUSTOM_WIFI_SIGNAL_BACKGROUND="blue"
# POWERLEVEL9K_CUSTOM_WIFI_SIGNAL_FOREGROUND="yellow"
#
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(custom_recording status root_indicator user dir dir_writable rbenv vcs newline)
#POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status background_jobs history time)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=()
POWERLEVEL9K_CUSTOM_RECORDING="echo \$( [[ \$ASCIINEMA_REC ]] && echo )"
POWERLEVEL9K_CUSTOM_RECORDING_BACKGROUND="black"
POWERLEVEL9K_CUSTOM_RECORDING_FOREGROUND="red"

# enable tmuxinator in zsh
source ~/git/other/tmuxinator/completion/tmuxinator.zsh

## my alias'
# vpn
alias vpn='/home/toniwarnecke/scripts/vpn_ctl'   	# show states for vpns 
# openstack-cli
alias os='openstack'                                    # for the openstack cli
alias os-source='source ~/openstack_rc_files/choose'    # to source an openstack-cl
# pview
alias pview='ssh cat-prod-secret pview '
# tks
alias wrms='~/.tks/tw_tks'                              # launch my local tks script
# keychain
alias keychain_unlock='keychain --nogui --quiet id_rsa' # unlock my keychain
# git my userhome
alias home='git --work-tree=/home/toniwarnecke --git-dir /home/toniwarnecke/git/other/my-client-config'
# asciinema
alias rec='python ${HOME}/scripts/rec_term.py '

## my user config
EMAIL=toniwarnecke@catalyst.net.nz
MYUSER=toniwarnecke
MYNAME="Toni Warnecke"

## python config
# virtualenvwrapper
WORKON_HOME=~/python_environments               # here is my python environments root
source /usr/local/bin/virtualenvwrapper.sh      # enables virtualenvwrapper
source ~/.autoenv/activate.sh                   # enables autoenv - executed .env when entering a dir an .env exists
AUTOENV_ENABLE_LEAVE=true                       # enables autoenv to execute .env.leave when leavin an dir and .env.leave exists
AUTOENV_ASSUME_YES=true                         # skip the authorisation of execute .env or .env.leave

