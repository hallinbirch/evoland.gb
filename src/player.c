#include "./sprite16.h"
#include "./map.h"

Sprite16* _player_sprite;

INT8 _player_walk_to_dx;
INT8 _player_walk_to_dy;
INT8 _player_walk_to_count;

void player_init() {
    _player_sprite = sprite16_new(0, 0, 80, 80);  // FIXME
    _player_walk_to_count = 0;
}

// -1 <= dx <= 1
// -1 <= dy <= 1
void player_walk_to_cell(INT8 dx, INT8 dy) {
    if (_player_walk_to_count) {
        return;
    }
    if (dx) {
        _player_walk_to_dx = dx;
        _player_walk_to_dy = 0;
        _player_walk_to_count = MAP_CELL_SIZE;
    } else if (dy) {
        _player_walk_to_dx = 0;
        _player_walk_to_dy = dy;
        _player_walk_to_count = MAP_CELL_SIZE;
    }
}

void player_loop() {
    if (_player_walk_to_count) {
        _player_walk_to_count -= 1;
        map_scroll(_player_walk_to_dx, _player_walk_to_dy);
    }
}
