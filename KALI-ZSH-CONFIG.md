Add these to the end of your `~/.zshrc` to make screenshots for the OSCP easier.

## time and tun0 host

```zsh
setopt PROMPT_SUBST

function get_tun0_ip() {
    local tun0_ip
    tun0_ip=$(ip -4 addr show tun0 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
    echo "${tun0_ip:-Down}"
}

function oscp_rprompt() {
    local tun0="%F{cyan}tun0:%F{white}$(get_tun0_ip)%f"
    local target="%F{cyan}target:%F{white}${TARGET:--}%f"
    local ts="%F{cyan}$(date '+%m-%d-%y') %*%f"
    echo "$tun0 | $target | $ts"
}

RPROMPT='$(oscp_rprompt)'
```

Set your target IP with:

```zsh
export TARGET=10.10.10.1
```