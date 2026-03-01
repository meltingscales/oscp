Add these to the end of your `~/.zshrc` to make screenshots for the OSCP easier.

## time and tun0 host

```
function get_tun0_ip() {
    # Extract IP, default to "Down" if not found
    local tun0_ip=$(ip -4 addr show tun0 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}' || echo "Down")
    echo "%F{cyan}tun0:%F{white}$tun0_ip %F{cyan}| Date:%F{white} $(date '+%Y-%m-%d %H:%M')%f"
}


RPROMPT='$(get_tun0_ip) [%D{%Y-%m-%d %H:%M:%S}]'
```