function getIntTime() {
    let d = new Date()
    let _M = d.getMonth() + 1
    let M = _M < 10 ? '0' + _M : _M
    let D = d.getDate() < 10 ? '0' + d.getDate() : d.getDate()
    let H = d.getHours() < 10 ? '0' + d.getHours() : d.getHours()
    let m = d.getMinutes() < 10 ? '0' + d.getMinutes() : d.getMinutes()
    return parseInt(d.getFullYear()+ M + D  + H  + m)
}