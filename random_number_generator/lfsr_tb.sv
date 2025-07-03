module lfsr_tb;

    logic clk = 0;
    logic reset = 0;
    logic enable = 0;
    logic [8:0] rand_num;

    // File handle
    integer file;

    // Instantiate LFSR
    lfsr uut (
        .clk(clk),
        .reset(reset),
        .enable(enable),
        .out(rand_num)
    );

    // Clock generation
    always #5 clk = ~clk;

    initial begin
        file = $fopen("lfsr_output.csv", "w");
        $fdisplay(file, "Cycle,Value");

        reset = 0;
        #10;

        reset = 1;
        enable = 1;

        for (int i = 0; i < 100000; i++) begin
            @(posedge clk);
            $fdisplay(file, "%0d,%b", i, rand_num);
        end

        // Close file and end
        $fclose(file);
        $finish;
    end

endmodule
