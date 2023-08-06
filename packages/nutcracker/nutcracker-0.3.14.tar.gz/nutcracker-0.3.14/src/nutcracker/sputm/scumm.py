#!/usr/bin/env python3
import io
import operator
from collections import deque
from functools import partial
from itertools import takewhile

from nutcracker.utils.funcutils import grouper, flatten

    # SCUMM 6.0
    # /* 00 */
	# OPCODE(0x00, o6_pushByte);
	# OPCODE(0x01, o6_pushWord);
	# OPCODE(0x02, o6_pushByteVar);
	# OPCODE(0x03, o6_pushWordVar);
	# /* 04 */
	# OPCODE(0x06, o6_byteArrayRead);
	# OPCODE(0x07, o6_wordArrayRead);
	# /* 08 */
	# OPCODE(0x0a, o6_byteArrayIndexedRead);
	# OPCODE(0x0b, o6_wordArrayIndexedRead);
	# /* 0C */
	# OPCODE(0x0c, o6_dup);
	# OPCODE(0x0d, o6_not);
	# OPCODE(0x0e, o6_eq);
	# OPCODE(0x0f, o6_neq);
	# /* 10 */
	# OPCODE(0x10, o6_gt);
	# OPCODE(0x11, o6_lt);
	# OPCODE(0x12, o6_le);
	# OPCODE(0x13, o6_ge);
	# /* 14 */
	# OPCODE(0x14, o6_add);
	# OPCODE(0x15, o6_sub);
	# OPCODE(0x16, o6_mul);
	# OPCODE(0x17, o6_div);
	# /* 18 */
	# OPCODE(0x18, o6_land);
	# OPCODE(0x19, o6_lor);
	# OPCODE(0x1a, o6_pop);
	# /* 1C */
	# /* 20 */
	# /* 24 */
	# /* 28 */
	# /* 2C */
	# /* 30 */
	# /* 34 */
	# /* 38 */
	# /* 3C */
	# /* 40 */
	# OPCODE(0x42, o6_writeByteVar);
	# OPCODE(0x43, o6_writeWordVar);
	# /* 44 */
	# OPCODE(0x46, o6_byteArrayWrite);
	# OPCODE(0x47, o6_wordArrayWrite);
	# /* 48 */
	# OPCODE(0x4a, o6_byteArrayIndexedWrite);
	# OPCODE(0x4b, o6_wordArrayIndexedWrite);
	# /* 4C */
	# OPCODE(0x4e, o6_byteVarInc);
	# OPCODE(0x4f, o6_wordVarInc);
	# /* 50 */
	# OPCODE(0x52, o6_byteArrayInc);
	# OPCODE(0x53, o6_wordArrayInc);
	# /* 54 */
	# OPCODE(0x56, o6_byteVarDec);
	# OPCODE(0x57, o6_wordVarDec);
	# /* 58 */
	# OPCODE(0x5a, o6_byteArrayDec);
	# OPCODE(0x5b, o6_wordArrayDec);
	# /* 5C */
	# OPCODE(0x5c, o6_if);
	# OPCODE(0x5d, o6_ifNot);
	# OPCODE(0x5e, o6_startScript);
	# OPCODE(0x5f, o6_startScriptQuick);
	# /* 60 */
	# OPCODE(0x60, o6_startObject);
	# OPCODE(0x61, o6_drawObject);
	# OPCODE(0x62, o6_drawObjectAt);
	# OPCODE(0x63, o6_drawBlastObject);
	# /* 64 */
	# OPCODE(0x64, o6_setBlastObjectWindow);
	# OPCODE(0x65, o6_stopObjectCode);
	# OPCODE(0x66, o6_stopObjectCode);
	# OPCODE(0x67, o6_endCutscene);
	# /* 68 */
	# OPCODE(0x68, o6_cutscene);
	# OPCODE(0x69, o6_stopMusic);
	# OPCODE(0x6a, o6_freezeUnfreeze);
	# OPCODE(0x6b, o6_cursorCommand);
	# /* 6C */
	# OPCODE(0x6c, o6_breakHere);
	# OPCODE(0x6d, o6_ifClassOfIs);
	# OPCODE(0x6e, o6_setClass);
	# OPCODE(0x6f, o6_getState);
	# /* 70 */
	# OPCODE(0x70, o6_setState);
	# OPCODE(0x71, o6_setOwner);
	# OPCODE(0x72, o6_getOwner);
	# OPCODE(0x73, o6_jump);
	# /* 74 */
	# OPCODE(0x74, o6_startSound);
	# OPCODE(0x75, o6_stopSound);
	# OPCODE(0x76, o6_startMusic);
	# OPCODE(0x77, o6_stopObjectScript);
	# /* 78 */
	# OPCODE(0x78, o6_panCameraTo);
	# OPCODE(0x79, o6_actorFollowCamera);
	# OPCODE(0x7a, o6_setCameraAt);
	# OPCODE(0x7b, o6_loadRoom);
	# /* 7C */
	# OPCODE(0x7c, o6_stopScript);
	# OPCODE(0x7d, o6_walkActorToObj);
	# OPCODE(0x7e, o6_walkActorTo);
	# OPCODE(0x7f, o6_putActorAtXY);
	# /* 80 */
	# OPCODE(0x80, o6_putActorAtObject);
	# OPCODE(0x81, o6_faceActor);
	# OPCODE(0x82, o6_animateActor);
	# OPCODE(0x83, o6_doSentence);
	# /* 84 */
	# OPCODE(0x84, o6_pickupObject);
	# OPCODE(0x85, o6_loadRoomWithEgo);
	# OPCODE(0x87, o6_getRandomNumber);
	# /* 88 */
	# OPCODE(0x88, o6_getRandomNumberRange);
	# OPCODE(0x8a, o6_getActorMoving);
	# OPCODE(0x8b, o6_isScriptRunning);
	# /* 8C */
	# OPCODE(0x8c, o6_getActorRoom);
	# OPCODE(0x8d, o6_getObjectX);
	# OPCODE(0x8e, o6_getObjectY);
	# OPCODE(0x8f, o6_getObjectOldDir);
	# /* 90 */
	# OPCODE(0x90, o6_getActorWalkBox);
	# OPCODE(0x91, o6_getActorCostume);
	# OPCODE(0x92, o6_findInventory);
	# OPCODE(0x93, o6_getInventoryCount);
	# /* 94 */
	# OPCODE(0x94, o6_getVerbFromXY);
	# OPCODE(0x95, o6_beginOverride);
	# OPCODE(0x96, o6_endOverride);
	# OPCODE(0x97, o6_setObjectName);
	# /* 98 */
	# OPCODE(0x98, o6_isSoundRunning);
	# OPCODE(0x99, o6_setBoxFlags);
	# OPCODE(0x9a, o6_createBoxMatrix);
	# OPCODE(0x9b, o6_resourceRoutines);
	# /* 9C */
	# OPCODE(0x9c, o6_roomOps);
	# OPCODE(0x9d, o6_actorOps);
	# OPCODE(0x9e, o6_verbOps);
	# OPCODE(0x9f, o6_getActorFromXY);
	# /* A0 */
	# OPCODE(0xa0, o6_findObject);
	# OPCODE(0xa1, o6_pseudoRoom);
	# OPCODE(0xa2, o6_getActorElevation);
	# OPCODE(0xa3, o6_getVerbEntrypoint);
	# /* A4 */
	# OPCODE(0xa4, o6_arrayOps);
	# OPCODE(0xa5, o6_saveRestoreVerbs);
	# OPCODE(0xa6, o6_drawBox);
	# OPCODE(0xa7, o6_pop);
	# /* A8 */
	# OPCODE(0xa8, o6_getActorWidth);
	# OPCODE(0xa9, o6_wait);
	# OPCODE(0xaa, o6_getActorScaleX);
	# OPCODE(0xab, o6_getActorAnimCounter);
	# /* AC */
	# OPCODE(0xac, o6_soundKludge);
	# OPCODE(0xad, o6_isAnyOf);
	# OPCODE(0xae, o6_systemOps);
	# OPCODE(0xaf, o6_isActorInBox);
	# /* B0 */
	# OPCODE(0xb0, o6_delay);
	# OPCODE(0xb1, o6_delaySeconds);
	# OPCODE(0xb2, o6_delayMinutes);
	# OPCODE(0xb3, o6_stopSentence);
	# /* B4 */
	# OPCODE(0xb4, o6_printLine);
	# OPCODE(0xb5, o6_printText);
	# OPCODE(0xb6, o6_printDebug);
	# OPCODE(0xb7, o6_printSystem);
	# /* B8 */
	# OPCODE(0xb8, o6_printActor);
	# OPCODE(0xb9, o6_printEgo);
	# OPCODE(0xba, o6_talkActor);
	# OPCODE(0xbb, o6_talkEgo);
	# /* BC */
	# OPCODE(0xbc, o6_dimArray);
	# OPCODE(0xbd, o6_dummy);
	# OPCODE(0xbe, o6_startObjectQuick);
	# OPCODE(0xbf, o6_startScriptQuick2);
	# /* C0 */
	# OPCODE(0xc0, o6_dim2dimArray);
	# /* C4 */
	# OPCODE(0xc4, o6_abs);
	# OPCODE(0xc5, o6_distObjectObject);
	# OPCODE(0xc6, o6_distObjectPt);
	# OPCODE(0xc7, o6_distPtPt);
	# /* C8 */
	# OPCODE(0xc8, o6_kernelGetFunctions);
	# OPCODE(0xc9, o6_kernelSetFunctions);
	# OPCODE(0xca, o6_delayFrames);
	# OPCODE(0xcb, o6_pickOneOf);
	# /* CC */
	# OPCODE(0xcc, o6_pickOneOfDefault);
	# OPCODE(0xcd, o6_stampObject);
	# /* D0 */
	# OPCODE(0xd0, o6_getDateTime);
	# OPCODE(0xd1, o6_stopTalking);
	# OPCODE(0xd2, o6_getAnimateVariable);
	# /* D4 */
	# OPCODE(0xd4, o6_shuffle);
	# OPCODE(0xd5, o6_jumpToScript);
	# OPCODE(0xd6, o6_band);
	# OPCODE(0xd7, o6_bor);
	# /* D8 */
	# OPCODE(0xd8, o6_isRoomScriptRunning);
	# /* DC */
	# OPCODE(0xdd, o6_findAllObjects);
	# /* E0 */
	# OPCODE(0xe1, o6_getPixel);
	# OPCODE(0xe3, o6_pickVarRandom);
	# /* E4 */
	# OPCODE(0xe4, o6_setBoxSet);
	# /* E8 */
	# /* EC */
	# OPCODE(0xec, o6_getActorLayer);
	# OPCODE(0xed, o6_getObjectNewDir);

    # SCUMM 6.0HE
    # _opcodes[0x63].setProc(0, 0);
	# _opcodes[0x64].setProc(0, 0);
	# OPCODE(0x70, o60_setState);
	# _opcodes[0x9a].setProc(0, 0);
	# OPCODE(0x9c, o60_roomOps);
	# OPCODE(0x9d, o60_actorOps);
	# _opcodes[0xac].setProc(0, 0);
	# OPCODE(0xbd, o6_stopObjectCode);
	# OPCODE(0xc8, o60_kernelGetFunctions);
	# OPCODE(0xc9, o60_kernelSetFunctions);
	# OPCODE(0xd9, o60_closeFile);
	# OPCODE(0xda, o60_openFile);
	# OPCODE(0xdb, o60_readFile);
	# OPCODE(0xdc, o60_writeFile);
	# OPCODE(0xde, o60_deleteFile);
	# OPCODE(0xdf, o60_rename);
	# OPCODE(0xe0, o60_soundOps);
	# OPCODE(0xe2, o60_localizeArrayToScript);
	# OPCODE(0xe9, o60_seekFilePos);
	# OPCODE(0xea, o60_redimArray);
	# OPCODE(0xeb, o60_readFilePos);
	# _opcodes[0xec].setProc(0, 0);
	# _opcodes[0xed].setProc(0, 0);

    # SCUMM 7.0
	# OPCODE(0x74, o70_soundOps);
	# OPCODE(0x84, o70_pickupObject);
	# OPCODE(0x8c, o70_getActorRoom);
	# OPCODE(0x9b, o70_resourceRoutines);
	# OPCODE(0xae, o70_systemOps);
	# OPCODE(0xee, o70_getStringLen);
	# OPCODE(0xf2, o70_isResourceLoaded);
	# OPCODE(0xf3, o70_readINI);
	# OPCODE(0xf4, o70_writeINI);
	# OPCODE(0xf9, o70_createDirectory);
	# OPCODE(0xfa, o70_setSystemMessage);

    # SCUMM 7.1
    # OPCODE(0xc9, o71_kernelSetFunctions);
	# OPCODE(0xec, o71_copyString);
	# OPCODE(0xed, o71_getStringWidth);
	# OPCODE(0xef, o71_appendString);
	# OPCODE(0xf0, o71_concatString);
	# OPCODE(0xf1, o71_compareString);
	# OPCODE(0xf5, o71_getStringLenForWidth);
	# OPCODE(0xf6, o71_getCharIndexInString);
	# OPCODE(0xf7, o71_findBox);
	# OPCODE(0xfb, o71_polygonOps);
	# OPCODE(0xfc, o71_polygonHit);

    # SCUMM 7.2
	# OPCODE(0x02, o72_pushDWord);
	# OPCODE(0x04, o72_getScriptString);
	# _opcodes[0x0a].setProc(0, 0);
	# OPCODE(0x1b, o72_isAnyOf);
	# _opcodes[0x42].setProc(0, 0);
	# _opcodes[0x46].setProc(0, 0);
	# _opcodes[0x4a].setProc(0, 0);
	# _opcodes[0x4e].setProc(0, 0);
	# OPCODE(0x50, o72_resetCutscene);
	# OPCODE(0x52, o72_findObjectWithClassOf);
	# OPCODE(0x54, o72_getObjectImageX);
	# OPCODE(0x55, o72_getObjectImageY);
	# OPCODE(0x56, o72_captureWizImage);
	# OPCODE(0x58, o72_getTimer);
	# OPCODE(0x59, o72_setTimer);
	# OPCODE(0x5a, o72_getSoundPosition);
	# OPCODE(0x5e, o72_startScript);
	# OPCODE(0x60, o72_startObject);
	# OPCODE(0x61, o72_drawObject);
	# OPCODE(0x62, o72_printWizImage);
	# OPCODE(0x63, o72_getArrayDimSize);
	# OPCODE(0x64, o72_getNumFreeArrays);
	# _opcodes[0x97].setProc(0, 0);	// was: o6_setObjectName
	# OPCODE(0x9c, o72_roomOps);
	# OPCODE(0x9d, o72_actorOps);
	# OPCODE(0x9e, o72_verbOps);
	# OPCODE(0xa0, o72_findObject);
	# OPCODE(0xa4, o72_arrayOps);
	# OPCODE(0xae, o72_systemOps);
	# OPCODE(0xba, o72_talkActor);
	# OPCODE(0xbb, o72_talkEgo);
	# OPCODE(0xbc, o72_dimArray);
	# OPCODE(0xc0, o72_dim2dimArray);
	# OPCODE(0xc1, o72_traceStatus);
	# OPCODE(0xc8, o72_kernelGetFunctions);
	# OPCODE(0xce, o72_drawWizImage);
	# OPCODE(0xcf, o72_debugInput);
	# OPCODE(0xd5, o72_jumpToScript);
	# OPCODE(0xda, o72_openFile);
	# OPCODE(0xdb, o72_readFile);
	# OPCODE(0xdc, o72_writeFile);
	# OPCODE(0xdd, o72_findAllObjects);
	# OPCODE(0xde, o72_deleteFile);
	# OPCODE(0xdf, o72_rename);
	# OPCODE(0xe1, o72_getPixel);
	# OPCODE(0xe3, o72_pickVarRandom);
	# OPCODE(0xea, o72_redimArray);
	# OPCODE(0xf3, o72_readINI);
	# OPCODE(0xf4, o72_writeINI);
	# OPCODE(0xf8, o72_getResourceSize);
	# OPCODE(0xf9, o72_createDirectory);
	# OPCODE(0xfa, o72_setSystemMessage);


    # SCUMM 8.0
	# OPCODE(0x45, o80_createSound);
	# OPCODE(0x46, o80_getFileSize);
	# OPCODE(0x48, o80_stringToInt);
	# OPCODE(0x49, o80_getSoundVar);
	# OPCODE(0x4a, o80_localizeArrayToRoom);
	# OPCODE(0x4c, o80_sourceDebug);
	# OPCODE(0x4d, o80_readConfigFile);
	# OPCODE(0x4e, o80_writeConfigFile);
	# _opcodes[0x69].setProc(0, 0);
	# OPCODE(0x6b, o80_cursorCommand);
	# OPCODE(0x70, o80_setState);
	# _opcodes[0x76].setProc(0, 0);
	# _opcodes[0x94].setProc(0, 0);
	# _opcodes[0x9e].setProc(0, 0);
	# _opcodes[0xa5].setProc(0, 0);
	# OPCODE(0xac, o80_drawWizPolygon);
	# OPCODE(0xe0, o80_drawLine);
	# OPCODE(0xe3, o80_pickVarRandom);


stack = deque()

varname = {
    9: 'ego'
}

def var(num):
    return f'var {varname.get(num, num)}'

def statement(stream, *args):
    print(hex(stream.tell()), *args)

def cursor_command(stream):
    cmd = stream.read(1)
    statement(stream, 'cursor-command', ord(cmd))
    return cmd

def start_sound(stream):
    statement(stream, 'start-sound {')
    pop()
    pop()
    print('}')
    return b''

def stop_sound(stream):
    statement(stream, 'stop-sound {')
    pop()
    print('}')
    return b''

def push_byte(stream):
    cmd = stream.read(1)
    statement(stream, 'push-byte', ord(cmd), '{')
    push(cmd, 'bytecode')
    print('}')
    return cmd

def push_word(stream):
    cmd = stream.read(2)
    statement(stream, 'push-word', int.from_bytes(cmd, byteorder='little', signed=False), '{')
    push(cmd, 'bytecode')
    print('}')
    return cmd


def begin_override(stream):
    statement(stream, 'begin-override')
    return b''

def end_override(stream):
    statement(stream, 'end-override')
    return b''

def push(value, source, byteorder='little'):
    stack.append((value, source))
    numeric = 'unknown' if value is None else int.from_bytes(value, byteorder=byteorder, signed=False)
    print('    push (',numeric , source, ')')
    return numeric, source

def pop(byteorder='little'):
    value, source = stack.pop()
    numeric = 'unknown' if value is None else int.from_bytes(value, byteorder=byteorder, signed=False)
    print('    pop (',numeric , source, ')')
    return numeric, source

def start_script(stream):
    # args = get_stack_list(25)
    statement(stream, 'start-script {')
    script = pop()
    flags = pop()
    print('}')
    return b''

def jump(stream):
    offset = int.from_bytes(stream.read(2), byteorder='little', signed=True)
    statement(stream, 'jump', f'rel={hex(offset)}', f'abs={hex(offset + stream.tell())}')

def draw_wiz_image(stream):
    # args = get_stack_list(25)
    statement(stream, 'draw-wiz-image {')
    pop('big')
    pop('big')
    pop('big')
    pop('big')
    print('}')
    return b''

def write_word_var(stream):
    varnum = stream.read(2)
    statement(stream, 'write-word-var', int.from_bytes(varnum, byteorder='little', signed=False), ' {')
    pop()
    print('}')
    return varnum

def push_word_var(stream):
    varnum = stream.read(2)
    numeric = int.from_bytes(varnum, byteorder='little', signed=False)
    statement(stream, 'push-word-var', numeric, '{')
    push(None, var(numeric))
    print('}')
    return varnum

def push_byte_var(stream):
    varnum = stream.read(1)
    numeric = int.from_bytes(varnum, byteorder='little', signed=False)
    statement(stream, 'push-byte-var', numeric, '{')
    push(None, var(numeric))
    print('}')
    return varnum

def actor_ops(stream):

    ops = {
        76: 'set-actor-custom',
        78: 'set-sound',
        84: 'set-elevation',
        93: 'no-clip',
        95: 'ignore-boxes',
        197: 'set-current-actor',
        217: 'init'
    }

    cmd = stream.read(1)
    statement(stream, 'actor-ops', ops[ord(cmd)], '{')
    if ord(cmd) == 76:
        pop()
    if ord(cmd) == 78:
        get_list_args()
    if ord(cmd) == 84:
        pop()
    elif ord(cmd) == 197:
        pop()
    print('}')
    return cmd

def delay_frames(stream):
    statement(stream, 'delay-frames {')
    pop()
    print('}')
    return b''

def print_ego(stream):
    ops = {
        0xfe: 'begin'
    }
    cmd = stream.read(1)
    statement(stream, 'print-ego', ops[ord(cmd)], '{')
    push(None, var(9))
    print('}')
    return b''

def talk_ego(stream):
    statement(stream, 'talk-ego {')
    # push(None, f'var ego')
    # pop()
    print(readcstr(stream))
    print('}')
    return b''

def readcstr(stream):
    bound_read = iter(partial(stream.read, 1), b'')
    res = b''.join(takewhile(partial(operator.ne, b'\00'), bound_read))
    return res if res else None

def print_actor(stream):
    ops = {
        75: 'msg',
        0xf9: 'colors'
    }
    cmd = stream.read(1)
    statement(stream, 'print-actor', ops[ord(cmd)], '{')
    if ord(cmd) == 0xf9:
        pop()
    elif ord(cmd) == 75:
        print(readcstr(stream))
    print('}')
    return cmd

def wait(stream):
    ops = {
        169: 'for-message'
    }
    cmd = stream.read(1)
    statement(stream, 'wait', ops[ord(cmd)], '{')
    print('}')
    return cmd

def jump_if_not(stream):
    off = stream.read(2)
    offset = int.from_bytes(off, byteorder='little', signed=True)
    statement(stream, 'jump-if-not', f'rel={hex(offset)}', f'abs={hex(offset + stream.tell())}', '{')
    pop()
    print('}')
    return off

def jump_if(stream):
    off = stream.read(2)
    offset = int.from_bytes(off, byteorder='little', signed=True)
    statement(stream, 'jump-if', f'rel={hex(offset)}', f'abs={hex(offset + stream.tell())}', '{')
    pop()
    print('}')
    return off

def eq(stream):
    statement(stream, 'eq', '{')
    v1, s1 = pop()
    v2, s2 = pop()
    push(None, f'{v1} {s1} == {v2 } {s2}')
    print('}')
    return b''

def add(stream):
    statement(stream, 'add', '{')
    v1, s1 = pop()
    v2, s2 = pop()
    push(None, f'{v1} {s1} + {v2 } {s2}')
    print('}')
    return b''

def put_actor_at_obj(stream):
    statement(stream, 'put-actor-object', '{')
    pop()
    print('}')

def put_actor_xy(stream):
    statement(stream, 'put-actor-xy', '{')
    pop()
    pop()
    pop()
    pop()
    print('}')

def draw_box(stream):
    statement(stream, 'draw-box', '{')
    pop()
    pop()
    pop()
    pop()
    pop()
    print('}')

def rename(stream):
    statement(stream, 'rename', '{')
    print(readcstr(stream))
    print(readcstr(stream))
    print('}')
    return b''

def system_ops(stream):
    ops = {
        26: 'restore-background',
        158: 'restart',
        159: 'pause',
        160: 'quit'
    }

    cmd = stream.read(1)
    statement(stream, 'system-ops', ops[ord(cmd)])
    return cmd

def print_debug(stream):
    ops = {
        75: 'msg',
        0xf9: 'colors',
        0xfe: 'load-default'
    }
    cmd = stream.read(1)
    statement(stream, 'print-debug', ops[ord(cmd)], '{')
    if ord(cmd) == 0xf9:
        pop()
    elif ord(cmd) == 75:
        print(readcstr(stream))
    print('}')
    return cmd

def room_ops(stream):
    ops = {
        213: 'set-palette'
    }

    cmd = stream.read(1)
    statement(stream, 'room-ops', ops[ord(cmd)], '{')
    if ord(cmd) == 213:
        pop()
    print('}')
    return cmd

def kernel_set(stream):
    statement(stream, 'kernel-set', '{')
    pop()
    print('}')
    return b''

def get_list_args():
    num_args, _ = pop()
    for _ in range(num_args):
        pop()

def start_script_quick2(stream):
    # args = get_stack_list(25)
    statement(stream, 'start-script-quick2 {')
    get_list_args()
    print('}')
    return b''

def op_pop(stream):
    statement(stream, 'pop {')
    pop()
    print('}')

def stop_talking(stream):
    statement(stream, 'stop-talking')
    return b''

def resource_routine(stream):
    ops = {
        121: 'sound',
        122: 'custom',
        203: 'image'
    }

    cmd = stream.read(1)
    statement(stream, 'load-resource', ops[ord(cmd)], '{')
    pop('big')
    print('}')
    return cmd

def animate_actor(stream):
    statement(stream, 'animate-actor', '{')
    pop()
    pop()
    print('}')

def animate_var(stream):
    statement(stream, 'animate-var', '{')
    pop()
    pop()
    print('}')

def break_here(stream):
    statement(stream, 'break-here')

OPCODES = {
    0x00: push_byte,
    0x01: push_word,
    0x02: push_byte_var,
    0x03: push_word_var,
    0x0e: eq,
    0x14: add,
    0x43: write_word_var,
    0x5c: jump_if,
    0x5d: jump_if_not,
    0x5e: start_script,
    0x6b: cursor_command,
    0x6c: break_here,
    0x73: jump,
    0x74: start_sound,
    0x75: stop_sound,
    0x7f: put_actor_xy,
    0x80: put_actor_at_obj,
    0x82: animate_actor,
    0x95: begin_override,
    0x96: end_override,
    0x9b: resource_routine,
    0x9c: room_ops,
    0x9d: actor_ops,
    0xa6: draw_box,
    0xa7: op_pop,
    0xa9: wait,
    0xae: system_ops,
    0xb6: print_debug,
    0xb8: print_actor,
    0xb9: print_ego,
    0xbb: talk_ego,
    0xbf: start_script_quick2,
    0xc9: kernel_set,
    0xca: delay_frames,
    0xce: draw_wiz_image,
    0xd1: stop_talking,
    0xd2: animate_var,
    0xdf: rename,
}

def descumm(data: bytes):
    serial = data[0]
    print(f'Script #{serial}')
    with io.BytesIO(data[1:]) as stream:
        while True:
            next_byte = stream.read(1)
            if not next_byte:
                break
            opcode = ord(next_byte)
            try:
                OPCODES[opcode](stream)
            except Exception as e:
                print(f'{type(e)}: {str(e)}')
                print(stream.tell(), hex(opcode), hex(ord(stream.read(1))))
                raise e

if __name__ == '__main__':
    import argparse
    import os
    import glob

    from .preset import sputm

    parser = argparse.ArgumentParser(description='read smush file')
    parser.add_argument('files', nargs='+', help='files to read from')
    args = parser.parse_args()


    files = set(flatten(glob.iglob(r) for r in args.files))
    print(files)
    for filename in files:

        print(filename)

        with open(filename, 'rb') as res:
            resource = res.read()[8:]

        descumm(resource)
