     b68:	b008	bsr 0xb7c	{'entry':'main'}
     b6a:	0009	nop
     b6c:	b01d	bsr 0xbaa
     b6e:	0009	nop
     b70:	d34d	mov.l 0xca8,r3
     b72:	e500	mov #0,r5
     b74:	430b	jsr @r3
     b76:	6453	mov r5,r4
     b78:	affe	bra 0xb78	{'comment':'endless loop'}
     b7a:	0009	nop
