def main():
    mm = 0
    while mm < 100000:
        smm = '%06d' % mm
        sm = smm[:3]
        while len(sm)>1 and sm[0]=='0': sm = sm[1:]
        smmf = '.'.join((sm,smm[3:]))
        mmf = eval(smmf)
        cmf = round(mmf,2)
        scmf = smmf[:-1]
        if cmf != eval(scmf):
            print(repr((mm,smm,smmf,mmf,cmf,scmf,eval(scmf)))) 
        mm += 10
if __name__ == '__main__':
    main()
