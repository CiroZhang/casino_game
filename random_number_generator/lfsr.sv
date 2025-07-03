module lfsr (
    input  logic clk,
    input  logic reset,         
    input  logic enable,
    output logic [8:0] out
);

    logic [8:0] lfsr1, lfsr2;
    logic [8:0] mixed;

    always_ff @(posedge clk or negedge reset) begin
        if (!reset) begin
            lfsr1 <= 9'b000000001;
            lfsr2 <= 9'b000000010;
        end else if (enable) begin
            lfsr1 <= {lfsr1[7:0], lfsr1[8] ^ lfsr1[4]};
            lfsr2 <= {lfsr2[7:0], lfsr2[8] ^ lfsr2[5] ^ lfsr2[2]}; // different tap
        end
    end

    assign mixed = lfsr1 ^ {lfsr2[3:0], lfsr2[8:4]}; // mix shifted second LFSR
    assign out = mixed;

endmodule
