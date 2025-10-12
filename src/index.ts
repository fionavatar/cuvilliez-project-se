const binaryRegex = /^(0|1)+s/;

export class BitDescriptor {
    value: number;
    bits: number;

    constructor(value : number, bits: number){
        if(!(value > -1 && Number.isInteger(value))){
            throw new Error('value must be an integer > -1');
        }
        if(!(bits > 0 && Number.isInteger(value))){
            throw new Error('value must be an integer > 0');
        }

        this.value = value;
        this.bits = bits;
    }

    static fromString(value: string){
        if(!binaryRegex.test(value)){
            throw new Error('value must be a binary string');
        }

        return new BitsDescriptor(parseInt(value,2), value.length);

    }
}

export class BitPacker {
    static pack(BitDescriptors: Array<BitDescriptor>): Uint8Array{
        let size = 0;
        for (const bitDesc of BitDescriptors) {
            size += bitDesc.bits;
        }
        
    }
}