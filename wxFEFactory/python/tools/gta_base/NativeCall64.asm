.CODE

native_call PROC
    mov         r11,rsp
    mov         qword ptr [r11+18h],rbx
    mov         qword ptr [r11+20h],rbp
    push        rsi
    push        rdi
    push        r14
    sub         rsp,30h
    ; DWORD64* args = (DWORD64*)ctx->m_pArgs;
    mov         rsi,qword ptr [rcx+10h]
    mov         r14,rcx
    ; DWORD64 fflag = *args;
    mov         rdi,qword ptr [rsi]
    ; DWORD64 dwFunc = *++args;
    mov         rbp,qword ptr [rsi+8]
    ; DWORD64 dwThis = *++args;
    add         rsi,10h
    mov         qword ptr [r11-28h],rdi
    mov         rdx,qword ptr [rsi]
    ; ctx->m_nArgCount -= 3;
    add         dword ptr [rcx+8],0FFFFFFFDh
    mov         ebx,dword ptr [rcx+8]
    ; int count = ctx->m_nArgCount;
    ; int i = 0;
    ; bool *fflag_a = (bool*)&fflag;
    ; DWORD64 arg, result = 0;
    ; float fresult = 0;


    ; if (dwThis)
    test        rdx,rdx
    je          LABEL_1
    ; {
        ; dwThis ����rcx, ��һ����������rdx��xmm1���������ƣ����ĸ���֮��Ĳ���ͨ��ջ����
        ; ++count;
        inc         ebx
        ;   fflag <<= 1;
        shl         rdi, 8
        mov         qword ptr [r11-28h],rdi
    ;}
    ;else
    jmp         LABEL_2
    ; {
        ; ָ���һ������
        ; ++args;
        LABEL_1:
        add         rsi,8
    ; }
    ; ��ʱargsָ��dwThis���һ������

LABEL_2:
    ; DWORD stack_diff = 0;
    xor rdi, rdi
    ; ʣ��Ĳ���
    ; if (count >= 5)
    cmp         ebx,5
    jl          LABEL_4
    ; {
        ; args ָ����ĸ�����
        ; args += 4;
        ; ��Դ
        add rsi, 20h
        ; count -= 4
        sub rbx, 4
        ; stack_diff = (count << 3) + 0x20;
        ; ջҪԤ��20h���ֽ�
        lea         r10,[rbx*8+20h]
        mov rax, r10
        and rax, 0Fh
        test rax,rax
        je LABEL_3
        add r10, 8h
LABEL_3:
        sub rsp, r10
        ; Ŀ��
        mov rdi, rsp
        ; Ԥ��32�ֽ�
        add rdi, 20h
        ; ѭ������
        xor rcx, rcx
        mov ecx, ebx
        rep movsq

        ; ֮����rdi����stack_diff
        mov rdi, r10
        ; count += 4
        add ebx, 4
        ; �ٴ�ָ���һ������
        sub rsi, r10
        test rax, rax
        je LABEL_4
        ; ��ΪջҪ����16�ֽڣ�����ղ�Ϊ�˶�������8�����ڼ���ȥ
        add rsi, 8h
    ; }


    LABEL_4:
    ; if (count >= 1)
    cmp         ebx,1
    jl          LABEL_12
    ; {
        ; if (fflag_a[0])
        mov         al, byte ptr [r11-28h]
        cmp         al, 0
        je          LABEL_5
        ; {
            ; if (fflag_a[0] != 1) -> double
            cmp         al, 1
            je          LABEL_5_1
            movsd       xmm0, mmword ptr [rsi]
            jmp         LABEL_6
            LABEL_5_1:
            ; else -> float
            movss       xmm0, dword ptr [rsi]
            jmp         LABEL_6
        ; }
        ; else
        ; {
            LABEL_5:
            mov rcx, qword ptr[rsi]
        ; }
    ; }
LABEL_6:

    ; if (count >= 2)
    cmp         ebx,2
    jl          LABEL_12
    ; {
        ; if (fflag_a[1])
        mov         al, byte ptr [r11-27h]
        cmp         al, 0
        je          LABEL_7
        ; {
            ; if (fflag_a[1] != 1) -> double
            cmp         al, 1
            je          LABEL_7_1
            movsd xmm1, mmword ptr [rsi + 8h]
            jmp         LABEL_8
            LABEL_7_1:
            ; else -> float
            movss xmm1, dword ptr[rsi + 8h]
            jmp         LABEL_8
        ; }
        ; else
        ; {
            LABEL_7:
            mov rdx, qword ptr[rsi + 8h]
        ; }
    ; }

LABEL_8:
    ; if (count >= 3)
    cmp         ebx,3
    jl          LABEL_12
    ; {
        ; if (fflag_a[2])
        mov         al, byte ptr [r11-26h]
        cmp         al, 0
        je          LABEL_9
        ; {
            ; if (fflag_a[2] != 1) -> double
            cmp         al, 1
            je          LABEL_9_1
            movsd xmm2, mmword ptr [rsi + 10h]
            jmp         LABEL_10
            LABEL_9_1:
            ; else -> float
            movss xmm2, dword ptr[rsi + 10h]
            jmp         LABEL_10
        ; }
        ; else
        ; {
            LABEL_9:
            mov r8, qword ptr[rsi + 10h]
        ; }
    ; }

LABEL_10:
    ; if (count >= 4)
    cmp         ebx,4
    jl          LABEL_12
    ; {
        ; if (fflag_a[3])
        mov         al, byte ptr [r11-25h]
        cmp         al, 0
        je          LABEL_11
        ; {
            ; if (fflag_a[2] != 1) -> double
            cmp         al, 1
            je          LABEL_11_1
            movsd xmm3, mmword ptr [rsi + 18h]
            jmp         LABEL_12
            LABEL_11_1:
            ; else -> float
            movss xmm3, dword ptr[rsi + 18h]
            jmp         LABEL_12
        ; }
        ; else
        ; {
            LABEL_11:
            mov r9, qword ptr[rsi + 18h]
        ; }
    ; }


LABEL_12:
    call    rbp
    ; *(DWORD64*)(ctx->m_pReturn) = result;
    mov rcx,qword ptr [r14]
    mov qword ptr [rcx], rax
    ; *(float*)((DWORD64*)ctx->m_pReturn + 1) = fresult;
    movss  dword ptr [rcx+8], xmm0
    ; double result
    movsd  mmword ptr [rcx+10h], xmm0

    ; if (stack_diff)
    test        rdi,rdi
    je          LABEL_13
    ; {
        add rsp, rdi
    ; }
; }
    LABEL_13:
    add         rsp,30h
    pop         r14
    pop         rdi
    pop         rsi
    ret
native_call ENDP

END